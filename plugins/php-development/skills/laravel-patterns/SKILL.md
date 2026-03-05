---
name: laravel-patterns
description: Laravel implementation patterns — service providers, middleware, Form Requests, API Resources, Eloquent models, jobs with retry logic, events and listeners, and action classes. Use when writing Laravel application code.
---

# Laravel Implementation Patterns

Production-ready implementation patterns for Laravel 11+ applications. Every pattern is complete, copy-pasteable PHP code covering service providers, middleware, Form Requests, API Resources, Eloquent models, jobs, events, actions, and Blade templating.

## When to Use This Skill

- Writing or refactoring Laravel service providers, middleware, Form Requests, or API Resources
- Designing Eloquent models with relationships, casts, scopes, and accessors
- Implementing jobs, events, or listeners with queue integration
- Building action classes to encapsulate business logic
- Creating Blade layouts, components, and custom directives

## Core Concepts

1. **Service container is king.** Bind interfaces to implementations, resolve dependencies automatically, and keep classes decoupled.
2. **Convention over configuration.** Place files where the framework expects them and auto-discovery handles the rest.
3. **Thin controllers, fat services.** Controllers orchestrate; business logic belongs in Action classes, services, or domain objects.
4. **Blade is your template engine.** Use layouts, components, and directives for clean, reusable views.

## Quick Start

A minimal controller calling an Action class -- the recommended pattern for keeping controllers thin:

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers;

use App\Actions\CreateUserAction;
use App\Http\Requests\StoreUserRequest;
use App\Http\Resources\UserResource;

class UserController extends Controller
{
    public function store(
        StoreUserRequest $request,
        CreateUserAction $action,
    ): UserResource {
        $user = $action->execute($request->validated());

        return new UserResource($user);
    }
}
```

---

## Fundamental Patterns

### Pattern 1: Service Provider with Deferred Loading

Deferred providers only resolve when one of their provided bindings is actually requested, reducing boot overhead.

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use App\Contracts\PaymentGatewayInterface;
use App\Contracts\InvoiceGeneratorInterface;
use App\Services\StripePaymentGateway;
use App\Services\PdfInvoiceGenerator;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class PaymentServiceProvider extends ServiceProvider implements DeferrableProvider
{
    public function register(): void
    {
        $this->app->singleton(PaymentGatewayInterface::class, function ($app) {
            return new StripePaymentGateway(
                apiKey: config('services.stripe.secret'),
                webhookSecret: config('services.stripe.webhook_secret'),
                logger: $app->make('log'),
            );
        });

        $this->app->bind(InvoiceGeneratorInterface::class, function ($app) {
            return new PdfInvoiceGenerator(
                storagePath: storage_path('app/invoices'),
                gateway: $app->make(PaymentGatewayInterface::class),
            );
        });
    }

    public function boot(): void
    {
        $this->publishes([
            __DIR__ . '/../../config/payment.php' => config_path('payment.php'),
        ], 'payment-config');
    }

    /** @return array<int, string> */
    public function provides(): array
    {
        return [
            PaymentGatewayInterface::class,
            InvoiceGeneratorInterface::class,
        ];
    }
}
```

### Pattern 2: Middleware with Parameters

Parameterized middleware lets you reuse a single class across routes with different configurations. Register the alias in `bootstrap/app.php` (Laravel 11+).

```php
<?php

declare(strict_types=1);

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class RequireRole
{
    /** @param string ...$roles One or more role names passed via route definition */
    public function handle(Request $request, Closure $next, string ...$roles): Response
    {
        $user = $request->user();

        if (! $user) {
            abort(401, 'Authentication required.');
        }

        $userRoles = $user->roles->pluck('slug')->toArray();

        if (empty(array_intersect($userRoles, $roles))) {
            abort(403, sprintf(
                'This action requires one of the following roles: %s.',
                implode(', ', $roles),
            ));
        }

        return $next($request);
    }
}
```

Register in `bootstrap/app.php` (Laravel 11+):

```php
use App\Http\Middleware\RequireRole;
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withMiddleware(function (Middleware $middleware) {
        $middleware->alias([
            'role' => RequireRole::class,
        ]);
    })
    ->create();
```

Use on routes:

```php
// Single role
Route::get('/admin/dashboard', DashboardController::class)
    ->middleware('role:admin');

// Multiple roles (any match grants access)
Route::get('/reports', ReportController::class)
    ->middleware('role:admin,analyst,manager');
```

### Pattern 3: Form Request with Custom Validation

Form Requests centralize validation, authorization, and error messaging. They are auto-injected into controller methods by the service container.

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests;

use App\Models\Product;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

class StoreProductRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Product::class);
    }

    /** @return array<string, mixed> */
    public function rules(): array
    {
        return [
            'name' => [
                'required', 'string', 'min:3', 'max:255',
                Rule::unique('products', 'name')
                    ->where('tenant_id', $this->user()->tenant_id),
            ],
            'sku' => [
                'required', 'string', 'alpha_dash', 'max:64',
                Rule::unique('products', 'sku'),
            ],
            'price' => ['required', 'decimal:0,2', 'min:0.01', 'max:999999.99'],
            'category_id' => ['required', 'integer', 'exists:categories,id'],
            'tags' => ['sometimes', 'array', 'max:10'],
            'tags.*' => ['string', 'max:50'],
            'image' => [
                'sometimes',
                File::image()
                    ->max(5 * 1024)
                    ->dimensions(
                        Rule::dimensions()->minWidth(200)->minHeight(200)
                            ->maxWidth(4000)->maxHeight(4000)
                    ),
            ],
            'description' => ['nullable', 'string', 'max:5000'],
            'is_active' => ['boolean'],
        ];
    }

    /** @return array<string, string> */
    public function messages(): array
    {
        return [
            'name.unique' => 'A product with this name already exists in your organization.',
            'sku.unique' => 'This SKU is already in use. SKUs must be globally unique.',
            'price.min' => 'Price must be at least $0.01.',
            'tags.max' => 'You may assign a maximum of 10 tags.',
        ];
    }

    /** @return array<string, string> */
    public function attributes(): array
    {
        return [
            'category_id' => 'category',
            'is_active' => 'active status',
        ];
    }

    protected function prepareForValidation(): void
    {
        $this->merge([
            'sku' => strtoupper((string) $this->sku),
            'is_active' => $this->boolean('is_active'),
        ]);
    }
}
```

### Pattern 4: API Resource with Conditional Attributes

API Resources transform Eloquent models into JSON. Use `whenLoaded()` to include relationships only when eager-loaded, preventing N+1 queries.

```php
<?php

declare(strict_types=1);

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/** @mixin \App\Models\Product */
class ProductResource extends JsonResource
{
    /** @return array<string, mixed> */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'sku' => $this->sku,
            'price' => $this->price,
            'formatted_price' => $this->formatted_price,
            'is_active' => $this->is_active,
            'description' => $this->when(
                $request->routeIs('products.show'),
                $this->description,
            ),

            // Only included when the relationship was eager-loaded
            'category' => new CategoryResource($this->whenLoaded('category')),
            'tags' => TagResource::collection($this->whenLoaded('tags')),

            // Aggregate values -- only present when withCount()/withAvg() was used
            'reviews_count' => $this->whenCounted('reviews'),
            'average_rating' => $this->whenAggregated('reviews', 'rating', 'avg'),

            // Conditional pivot data
            'quantity' => $this->whenPivotLoaded('order_product', function () {
                return $this->pivot->quantity;
            }),

            // Auth-gated fields
            'cost' => $this->when(
                $request->user()?->can('viewCosts', $this->resource),
                fn () => $this->cost,
            ),

            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),

            'links' => [
                'self' => route('products.show', $this->resource),
            ],
        ];
    }
}
```

Usage in a controller:

```php
public function index(Request $request): AnonymousResourceCollection
{
    $products = Product::query()
        ->with(['category', 'tags'])
        ->withCount('reviews')
        ->withAvg('reviews', 'rating')
        ->paginate($request->integer('per_page', 15));

    return ProductResource::collection($products);
}
```

### Pattern 5: Eloquent Model with Casts, Relationships, and Scopes

A well-structured Eloquent model declares mass-assignment protection, casts, relationships, scopes, and accessors in a consistent order.

```php
<?php

declare(strict_types=1);

namespace App\Models;

use App\Enums\ProductStatus;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\SoftDeletes;

class Product extends Model
{
    use HasFactory;
    use SoftDeletes;

    // ── Mass assignment ──────────────────────────

    protected $fillable = [
        'name', 'sku', 'description', 'price', 'cost',
        'category_id', 'status', 'metadata', 'is_active', 'published_at',
    ];

    // ── Attribute casting ────────────────────────

    protected function casts(): array
    {
        return [
            'price' => 'decimal:2',
            'cost' => 'decimal:2',
            'is_active' => 'boolean',
            'metadata' => 'array',
            'status' => ProductStatus::class,
            'published_at' => 'immutable_datetime',
        ];
    }

    // ── Relationships ────────────────────────────

    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class)
            ->withTimestamps()
            ->withPivot('sort_order')
            ->orderByPivot('sort_order');
    }

    public function reviews(): HasMany
    {
        return $this->hasMany(Review::class);
    }

    // ── Scopes ───────────────────────────────────

    public function scopeActive(Builder $query): void
    {
        $query->where('is_active', true);
    }

    public function scopePublished(Builder $query): void
    {
        $query->where('status', ProductStatus::Published)
            ->whereNotNull('published_at')
            ->where('published_at', '<=', now());
    }

    public function scopePriceBetween(Builder $query, float $min, float $max): void
    {
        $query->whereBetween('price', [$min, $max]);
    }

    // ── Accessors (Laravel 11+ syntax) ───────────

    protected function formattedPrice(): Attribute
    {
        return Attribute::get(
            fn () => '$' . number_format((float) $this->price, 2),
        );
    }

    protected function profitMargin(): Attribute
    {
        return Attribute::get(function () {
            if (! $this->cost || $this->cost == 0) {
                return null;
            }

            return round((($this->price - $this->cost) / $this->price) * 100, 1);
        });
    }

    protected function name(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => $value,
            set: fn (string $value) => trim($value),
        );
    }
}
```

### Pattern 6: Job with Retry, Backoff, and Failure Handling

Jobs encapsulate async work. Configure retries, exponential backoff, timeouts, and failure callbacks for resilient queue processing.

```php
<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Models\Order;
use App\Services\ShippingProviderService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\Middleware\RateLimited;
use Illuminate\Queue\Middleware\WithoutOverlapping;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;
use Throwable;

class FulfillOrderJob implements ShouldQueue, ShouldBeUnique
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 5;
    public int $timeout = 120;
    public int $uniqueFor = 600;

    /** @return array<int, int> */
    public function backoff(): array
    {
        return [10, 30, 60, 120];
    }

    public function uniqueId(): string
    {
        return 'fulfill-order-' . $this->order->id;
    }

    public function __construct(
        public readonly Order $order,
    ) {
        $this->onQueue('fulfillment');
    }

    /** @return array<int, object> */
    public function middleware(): array
    {
        return [
            new RateLimited('shipping-api'),
            (new WithoutOverlapping($this->order->id))
                ->releaseAfter(60)
                ->expireAfter(300),
        ];
    }

    public function handle(ShippingProviderService $shipping): void
    {
        if ($this->order->status !== 'paid') {
            Log::warning('Order not in paid status, skipping.', [
                'order_id' => $this->order->id,
                'status' => $this->order->status,
            ]);

            return;
        }

        $tracking = $shipping->createShipment(
            address: $this->order->shipping_address,
            items: $this->order->items->toArray(),
            weight: $this->order->total_weight,
        );

        $this->order->update([
            'status' => 'shipped',
            'tracking_number' => $tracking->number,
            'tracking_url' => $tracking->url,
            'shipped_at' => now(),
        ]);
    }

    public function retryUntil(): \DateTime
    {
        return now()->addHours(6);
    }

    public function failed(?Throwable $exception): void
    {
        Log::error('Order fulfillment failed permanently.', [
            'order_id' => $this->order->id,
            'exception' => $exception?->getMessage(),
            'attempts' => $this->attempts(),
        ]);

        $this->order->update(['status' => 'fulfillment_failed']);
    }
}
```

Dispatch:

```php
FulfillOrderJob::dispatch($order);
FulfillOrderJob::dispatch($order)->delay(now()->addMinutes(5));
FulfillOrderJob::dispatchIf($order->is_paid, $order);
```

### Pattern 7: Event and Listener with Queued Listener

Events decouple the action from the reactions. Use queued listeners for side effects (emails, API calls, analytics) that should not block the request.

**Event class:**

```php
<?php

declare(strict_types=1);

namespace App\Events;

use App\Models\Order;
use App\Models\User;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderPlaced
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public readonly Order $order,
        public readonly User $customer,
        public readonly string $ipAddress,
    ) {}
}
```

**Queued listener:**

```php
<?php

declare(strict_types=1);

namespace App\Listeners;

use App\Events\OrderPlaced;
use App\Mail\OrderConfirmation;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Mail;
use Throwable;

class SendOrderConfirmationEmail implements ShouldQueue
{
    use InteractsWithQueue;

    public string $queue = 'notifications';
    public int $tries = 3;

    /** @return array<int, int> */
    public function backoff(): array
    {
        return [5, 30, 120];
    }

    public function shouldQueue(OrderPlaced $event): bool
    {
        return $event->customer->wants_email_notifications;
    }

    public function handle(OrderPlaced $event): void
    {
        Mail::to($event->customer->email)
            ->send(new OrderConfirmation(
                order: $event->order,
                customer: $event->customer,
            ));
    }

    public function failed(OrderPlaced $event, Throwable $exception): void
    {
        Log::error('Failed to send order confirmation email.', [
            'order_id' => $event->order->id,
            'error' => $exception->getMessage(),
        ]);
    }
}
```

**Synchronous listener (runs in the same request):**

```php
<?php

declare(strict_types=1);

namespace App\Listeners;

use App\Events\OrderPlaced;

class DecrementInventory
{
    public function handle(OrderPlaced $event): void
    {
        foreach ($event->order->items as $item) {
            $item->variant->decrement('stock_quantity', $item->quantity);
        }
    }
}
```

**Register and dispatch:**

```php
use Illuminate\Support\Facades\Event;

Event::listen(OrderPlaced::class, DecrementInventory::class);
Event::listen(OrderPlaced::class, SendOrderConfirmationEmail::class);

// Dispatch from anywhere
OrderPlaced::dispatch($order, $customer, $request->ip());
```

### Pattern 8: Action Class for Business Logic

Actions are single-responsibility classes that encapsulate one business operation. Easy to test, easy to reuse from controllers, jobs, and commands.

```php
<?php

declare(strict_types=1);

namespace App\Actions;

use App\Data\CreateUserData;
use App\Events\UserRegistered;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;

final class CreateUserAction
{
    public function __construct(
        private readonly AssignDefaultRoleAction $assignRole,
        private readonly ProvisionUserWorkspaceAction $provisionWorkspace,
    ) {}

    public function execute(CreateUserData|array $data): User
    {
        if (is_array($data)) {
            $data = CreateUserData::from($data);
        }

        return DB::transaction(function () use ($data) {
            $user = User::create([
                'name' => $data->name,
                'email' => $data->email,
                'password' => Hash::make($data->password),
                'timezone' => $data->timezone ?? config('app.timezone'),
            ]);

            $this->assignRole->execute($user);
            $this->provisionWorkspace->execute($user);

            UserRegistered::dispatch($user);

            return $user->refresh();
        });
    }
}
```

**Supporting Data Transfer Object:**

```php
<?php

declare(strict_types=1);

namespace App\Data;

final readonly class CreateUserData
{
    public function __construct(
        public string $name,
        public string $email,
        public string $password,
        public ?string $timezone = null,
    ) {}

    public static function from(array $data): self
    {
        return new self(
            name: $data['name'],
            email: $data['email'],
            password: $data['password'],
            timezone: $data['timezone'] ?? null,
        );
    }
}
```

**Usage from a controller and an Artisan command:**

```php
// Controller
public function store(StoreUserRequest $request, CreateUserAction $action): UserResource
{
    return new UserResource($action->execute($request->validated()));
}

// Artisan command
public function handle(CreateUserAction $action): int
{
    $user = $action->execute(new CreateUserData(
        name: $this->argument('name'),
        email: $this->argument('email'),
        password: $this->secret('Enter password'),
    ));

    $this->info("Created user #{$user->id}");

    return self::SUCCESS;
}
```

---

## Blade Templating Patterns

### Layouts with Stacks and Sections

Define a base layout and extend it with child views. Use `@stack` for page-specific scripts or styles.

**`resources/views/layouts/app.blade.php`:**

```blade
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>@yield('title', config('app.name'))</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    @stack('styles')
</head>
<body class="@yield('body-class', 'bg-gray-50')">
    @include('partials.navigation')

    <main>
        @yield('content')
    </main>

    @include('partials.footer')
    @stack('scripts')
</body>
</html>
```

**`resources/views/products/index.blade.php`:**

```blade
@extends('layouts.app')

@section('title', 'Products')

@section('content')
    <div class="container mx-auto px-4 py-8">
        @foreach ($products as $product)
            <x-product-card :product="$product" />
        @endforeach

        {{ $products->links() }}
    </div>
@endsection

@push('scripts')
    <script>console.log('Products page loaded');</script>
@endpush
```

### Anonymous Blade Components

Store anonymous components in `resources/views/components/`. They receive props via `@props` and render with `<x-name>` syntax.

**`resources/views/components/card.blade.php`:**

```blade
@props([
    'title' => '',
    'image' => null,
    'url' => '#',
    'badge' => null,
])

<article {{ $attributes->merge(['class' => 'bg-white rounded-lg shadow-md overflow-hidden']) }}>
    @if ($image)
        <a href="{{ $url }}">
            <img src="{{ $image }}" alt="{{ $title }}" class="w-full h-48 object-cover" loading="lazy" />
        </a>
    @endif

    <div class="p-6">
        @if ($badge)
            <span class="inline-block px-2 py-1 text-xs font-semibold bg-blue-50 text-blue-900 rounded mb-2">
                {{ $badge }}
            </span>
        @endif

        <h3 class="text-lg font-bold mb-2">
            <a href="{{ $url }}" class="hover:text-blue-500 transition-colors">{{ $title }}</a>
        </h3>

        @if ($slot->isNotEmpty())
            <div class="mt-4 pt-4 border-t border-gray-100">{{ $slot }}</div>
        @endif
    </div>
</article>
```

**Usage:**

```blade
<x-card title="My Article" :url="route('articles.show', $article)" :image="$article->image_url">
    <p class="text-sm text-gray-600">{{ $article->excerpt }}</p>
</x-card>
```

### Custom Blade Directives

Register custom directives in a service provider for clean, reusable template syntax.

```php
<?php

declare(strict_types=1);

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class BladeDirectivesServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        // @money(1999, 'USD') -- format a price
        Blade::directive('money', function (string $expression) {
            return "<?php echo '\\$' . number_format({$expression} / 100, 2); ?>";
        });

        // @datetime($carbon) -- format a Carbon instance
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ({$expression})->format('M j, Y \\a\\t g:ia'); ?>";
        });

        // @production ... @endproduction
        Blade::if('production', function () {
            return app()->environment('production');
        });

        // @feature('dark_mode') ... @endfeature
        Blade::if('feature', function (string $flag) {
            return config("features.{$flag}", false);
        });
    }
}
```

**Usage:**

```blade
<span>@money($product->price_cents)</span>
<time>@datetime($order->created_at)</time>

@production
    <script src="https://analytics.example.com/tracker.js"></script>
@endproduction

@feature('dark_mode')
    <link rel="stylesheet" href="{{ asset('css/dark.css') }}" />
@endfeature
```

---

## Best Practices Summary

1. **Use deferred service providers** for bindings not needed on every request. Implement `DeferrableProvider` and define `provides()`.

2. **Keep controllers thin.** Extract business logic into Action classes. Controllers validate (Form Request), orchestrate (Action), and transform (API Resource).

3. **Always use `whenLoaded()` in API Resources.** Never access relationships directly -- it causes silent N+1 queries when the relationship was not eager-loaded.

4. **Declare `$fillable` explicitly.** Never use `$guarded = []`. Whitelist every mass-assignable field.

5. **Configure job retry and failure handling.** Every job should define `$tries`, `backoff()`, `timeout`, and a `failed()` method.

6. **Use queued listeners for side effects.** Email, API calls, analytics, and audit logging should happen in queued listeners, not synchronously in controllers.

7. **Use Blade components over raw includes.** Components with `@props` enforce a typed interface and keep templates self-documenting.

8. **Register custom Blade directives for repeated patterns.** Wrapping formatting, environment checks, and feature flags in directives keeps templates clean.
