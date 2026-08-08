# TypeScript Cheat Sheet for Test Automation Engineers

> A fast, practical reference for QA engineers moving from manual testing (or plain JavaScript / Java) into Playwright with TypeScript.
> Every example is written the way you would actually write it inside a test framework.

---

## Table of Contents

| # | Section |
|---|---------|
| 1 | [What is TypeScript](#1-what-is-typescript) |
| 2 | [Setup in five minutes](#2-setup-in-five-minutes) |
| 3 | [Variables: let, const, var](#3-variables-let-const-var) |
| 4 | [Basic types: all the data types](#4-basic-types-all-the-data-types) |
| 5 | [Type inference](#5-type-inference) |
| 6 | [Arrays, tuples and objects](#6-arrays-tuples-and-objects) |
| 7 | [Special types: any, unknown, never, void, null, undefined](#7-special-types-any-unknown-never-void-null-undefined) |
| 8 | [Functions](#8-functions) |
| 9 | [Interfaces](#9-interfaces) |
| 10 | [Type aliases](#10-type-aliases) |
| 11 | [Interface vs type alias](#11-interface-vs-type-alias) |
| 12 | [Union and intersection types](#12-union-and-intersection-types) |
| 13 | [Literal types, narrowing and type guards](#13-literal-types-narrowing-and-type-guards) |
| 14 | [Enums](#14-enums) |
| 15 | [Classes and the Page Object Model](#15-classes-and-the-page-object-model) |
| 16 | [Generics](#16-generics) |
| 17 | [Type assertions](#17-type-assertions) |
| 18 | [Optional chaining and nullish coalescing](#18-optional-chaining-and-nullish-coalescing) |
| 19 | [Modules: import and export](#19-modules-import-and-export) |
| 20 | [Utility types](#20-utility-types) |
| 21 | [Async, await and Promises](#21-async-await-and-promises) |
| 22 | [Modern JavaScript essentials](#22-modern-javascript-essentials-you-will-use-daily) |
| 23 | [tsconfig.json explained](#23-tsconfigjson-explained) |
| 24 | [Typing test data, JSON and environment variables](#24-typing-test-data-json-and-environment-variables) |
| 25 | [Playwright specific TypeScript patterns](#25-playwright-specific-typescript-patterns) |
| 26 | [Common compiler errors and how to fix them](#26-common-compiler-errors-and-how-to-fix-them) |
| 27 | [Best practices](#27-best-practices) |
| 28 | [Common pitfalls](#28-common-pitfalls) |
| 29 | [Practice exercises](#29-practice-exercises) |
| 30 | [One page summary](#30-one-page-summary) |

---

## 1. What is TypeScript

TypeScript is JavaScript with a type system bolted on top. You write `.ts` files, the TypeScript compiler (`tsc`) checks them for type errors, and it strips the types out to produce plain JavaScript that Node or the browser runs.

```
your-test.ts  -->  tsc / ts-node  -->  your-test.js  -->  Node runs it
                        ^
                   type checking happens HERE, before anything executes
```

**Key facts:**

- TypeScript is a **superset** of JavaScript. Every valid `.js` file is a valid `.ts` file. You already know 80% of it.
- Types exist **only at compile time**. At runtime there are no types at all. This matters a lot: TypeScript cannot validate an API response for you at runtime.
- TypeScript never changes what your code does. It only tells you when your code does not make sense.

### Why it matters for test automation

| Problem in plain JavaScript | What TypeScript does about it |
|---|---|
| `page.getByRole('buton')` typo, fails at runtime after 30 seconds | Red squiggle in the editor before you run anything |
| You forget `await` on a Playwright call, test passes falsely | `no-floating-promises` lint rule catches it |
| Test data object is missing a field, test fails deep in a helper | Compiler flags the missing property immediately |
| You do not know what a helper function returns | Hover in VS Code and the editor tells you |
| Refactoring a page object breaks 40 tests silently | Compiler lists every broken call site |

**One line summary:** TypeScript moves failures from *test run time* to *typing time*. For a test framework that runs for 40 minutes in CI, that is an enormous feedback loop win.

---

## 2. Setup in five minutes

```bash
# New Playwright project, already TypeScript ready
npm init playwright@latest

# Adding TypeScript to an existing Node project
npm i -D typescript @types/node
npx tsc --init

# Type check without emitting JavaScript (what you run in CI)
npx tsc --noEmit

# Playwright compiles TypeScript for you, no build step needed
npx playwright test
```

**File extensions you will see:**

| Extension | Meaning |
|---|---|
| `.ts` | TypeScript source |
| `.d.ts` | Declaration file, types only, no implementation |
| `.spec.ts` / `.test.ts` | Playwright picks these up as test files by default |
| `.js` | Compiled output, usually gitignored |

**Pro tip:** Playwright uses its own transpiler (esbuild) and does **not** fail the run on type errors. Always add `tsc --noEmit` as a separate step in Jenkins / GitHub Actions / ADO, otherwise type safety silently stops protecting you.

---

## 3. Variables: let, const, var

```ts
const baseUrl = 'https://staging.example.com'; // cannot be reassigned, use by default
let attempts = 0;                              // reassignable
attempts = attempts + 1;

var oldStyle = 'avoid';                        // function scoped, legacy, do not use
```

`const` prevents **reassignment**, not **mutation**:

```ts
const users = ['nigel'];
users.push('ravindu');       // legal, the array contents changed
// users = ['someone else']; // Error: cannot assign to 'users'
```

**Rule of thumb:** `const` everywhere, switch to `let` only when the compiler complains.

---

## 4. Basic types: all the data types

### 4.1 Primitives

```ts
let username: string = 'nigel';
let retryCount: number = 3;          // integers and floats are both 'number'
let isLoggedIn: boolean = true;
let sessionId: null = null;
let notSet: undefined = undefined;
let userId: bigint = 9007199254740993n;
let uniqueKey: symbol = Symbol('key');
```

### 4.2 The full type reference table

| Type | Example value | When you use it in tests |
|---|---|---|
| `string` | `'Login'` | Selectors, URLs, expected text, usernames |
| `number` | `30_000` | Timeouts, retry counts, HTTP status codes |
| `boolean` | `true` | Feature flags, headless mode, visibility results |
| `bigint` | `123n` | Rare, very large IDs from a database |
| `symbol` | `Symbol('id')` | Rare, unique object keys |
| `null` | `null` | Explicitly "no value", common in API JSON |
| `undefined` | `undefined` | Value not provided or not yet set |
| `any` | anything | Escape hatch, avoid |
| `unknown` | anything | Safe `any`, for untrusted API responses |
| `void` | nothing | Function return type when it returns nothing |
| `never` | nothing ever | Function that always throws or never ends |
| `object` | `{}` | Non primitive, rarely used directly |
| `Array<T>` / `T[]` | `['a','b']` | Lists of test data |
| tuple | `[200, 'OK']` | Fixed length pairs |
| `Record<K, V>` | `{ a: 1 }` | Dictionaries, header maps |
| `Date` | `new Date()` | Time based assertions |
| `RegExp` | `/order-\d+/` | Text and URL matching |
| `Promise<T>` | `Promise<string>` | Every async function |

### 4.3 Real test framework examples

```ts
const timeout: number = 30_000;               // underscore is just readability
const browserName: string = 'chromium';
const headless: boolean = process.env.CI === 'true';
const expectedStatuses: number[] = [200, 201, 204];
const launchedAt: Date = new Date();
const orderIdPattern: RegExp = /^ORD-\d{6}$/;
```

---

## 5. Type inference

TypeScript works out the type on its own most of the time. **Do not annotate what is obvious.**

```ts
// Redundant, noisy
const title: string = 'Checkout';

// Idiomatic, TypeScript already knows it is a string
const title = 'Checkout';
```

Annotate when TypeScript cannot know, or when you want to constrain:

```ts
// TS cannot infer an empty array, it becomes any[]
const failedTests: string[] = [];

// You want a wider type than the inferred literal
let environment: 'dev' | 'qa' | 'prod' = 'qa';

// Function parameters are ALWAYS annotated, TS cannot guess them
function buildUrl(path: string, env: string): string {
  return `https://${env}.example.com/${path}`;
}
```

**Small but important:** `const` infers a *literal* type, `let` infers a *wide* type.

```ts
const env1 = 'qa';   // type is exactly 'qa'
let env2 = 'qa';     // type is string
```

---

## 6. Arrays, tuples and objects

### 6.1 Arrays

```ts
const usernames: string[] = ['nigel', 'ravindu', 'himasha'];
const statusCodes: Array<number> = [200, 404];   // same thing, generic syntax
const mixed: (string | number)[] = ['ORD-1', 42];

// Read only, cannot push or splice
const environments: readonly string[] = ['dev', 'qa', 'prod'];

// Array of objects, the shape of most test data files
const users: { username: string; role: string }[] = [
  { username: 'nigel', role: 'admin' },
  { username: 'ravindu', role: 'clinician' },
];
```

Useful array methods you will use constantly:

```ts
const ids = users.map(u => u.username);                 // transform
const admins = users.filter(u => u.role === 'admin');   // subset
const found = users.find(u => u.username === 'nigel');  // first match or undefined
const hasAdmin = users.some(u => u.role === 'admin');   // boolean
const allNamed = users.every(u => u.username.length > 0);
const total = statusCodes.reduce((sum, s) => sum + s, 0);
```

### 6.2 Tuples: fixed length, fixed order

```ts
const credentials: [string, string] = ['nigel', 'Passw0rd!'];
const [user, pass] = credentials;

// Named tuple elements, much more readable
type ApiResult = [status: number, body: string];
const result: ApiResult = [200, '{"ok":true}'];
```

### 6.3 Object types

```ts
// Inline object type
const patient: { id: number; name: string; nhsNumber?: string } = {
  id: 1,
  name: 'John Smith',
};
// nhsNumber has a '?' so it is optional

// Nested objects
const config: {
  baseUrl: string;
  auth: { username: string; password: string };
  retries: number;
} = {
  baseUrl: 'https://qa.example.com',
  auth: { username: 'nigel', password: 'secret' },
  retries: 2,
};
```

Once an object type is used more than once, move it to an `interface` or `type` (see sections 9 and 10). Inline object types are for one off use only.

### 6.4 readonly properties

```ts
interface TestConfig {
  readonly baseUrl: string;   // set once, cannot be changed later
  retries: number;
}

const cfg: TestConfig = { baseUrl: 'https://qa.example.com', retries: 2 };
cfg.retries = 3;              // fine
// cfg.baseUrl = 'other';     // Error: read only property
```

---

## 7. Special types: any, unknown, never, void, null, undefined

### 7.1 `any` turns type checking off

```ts
let response: any = await api.get('/patients');
response.thisMethodDoesNotExist();   // compiles, explodes at runtime
```

`any` is contagious and silently disables every protection TypeScript gives you. Treat every `any` in a code review as a bug until proven otherwise.

### 7.2 `unknown` is the safe version of `any`

```ts
const body: unknown = await response.json();

// body.patients;                      // Error: object is of type 'unknown'

if (typeof body === 'object' && body !== null && 'patients' in body) {
  // Narrowed, now safe to use
  console.log((body as { patients: unknown[] }).patients.length);
}
```

Use `unknown` for anything crossing a trust boundary: API responses, JSON files, `JSON.parse` results, caught errors.

### 7.3 `void`: the function returns nothing useful

```ts
async function login(page: Page, user: string, pass: string): Promise<void> {
  await page.getByLabel('Username').fill(user);
  await page.getByLabel('Password').fill(pass);
  await page.getByRole('button', { name: 'Sign in' }).click();
}
```

### 7.4 `never`: this never returns normally

```ts
function fail(message: string): never {
  throw new Error(message);
}

// Also used for exhaustiveness checking, see section 13
```

### 7.5 `null` and `undefined` under `strictNullChecks`

With `strict: true`, `null` and `undefined` are not assignable to other types. This is the single most valuable setting in TypeScript.

```ts
const text: string | null = await page.locator('h1').textContent();
// Playwright's textContent() genuinely can return null

// console.log(text.toUpperCase());  // Error: 'text' is possibly 'null'

console.log(text?.toUpperCase());    // safe, see section 18
```

---

## 8. Functions

### 8.1 The shapes

```ts
// Named function
function toTitleCase(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

// Arrow function, the style used in most modern frameworks
const toSlug = (value: string): string => value.toLowerCase().replace(/\s+/g, '-');

// Implicit return, no braces needed for a single expression
const double = (n: number): number => n * 2;

// Async function, ALWAYS returns a Promise
async function getTitle(page: Page): Promise<string> {
  return page.title();
}
```

### 8.2 Optional, default and rest parameters

```ts
// Optional parameter, marked with ?
function buildUrl(path: string, env?: string): string {
  return `https://${env ?? 'qa'}.example.com${path}`;
}

// Default parameter, cleaner than optional when you have a sensible default
function waitFor(page: Page, selector: string, timeout = 30_000) {
  return page.locator(selector).waitFor({ timeout });
}

// Rest parameters, any number of arguments
function logSteps(testName: string, ...steps: string[]): void {
  steps.forEach((s, i) => console.log(`${testName} step ${i + 1}: ${s}`));
}

logSteps('Login', 'open page', 'fill form', 'submit');
```

**Rule:** optional parameters must come after required ones.

### 8.3 Object parameters, the pattern you should prefer

Three booleans in a row is unreadable. Use an options object.

```ts
// Hard to call correctly
// createPatient('John', true, false, true);

interface CreatePatientOptions {
  name: string;
  isUrgent?: boolean;
  sendSms?: boolean;
  active?: boolean;
}

function createPatient({ name, isUrgent = false, sendSms = false, active = true }: CreatePatientOptions) {
  // ...
}

createPatient({ name: 'John', isUrgent: true });  // self documenting at the call site
```

### 8.4 Function types

```ts
// A variable that holds a function
type Validator = (value: string) => boolean;

const isNhsNumber: Validator = (value) => /^\d{10}$/.test(value);

// A function that takes a function (callback)
async function retry(action: () => Promise<void>, attempts = 3): Promise<void> {
  for (let i = 1; i <= attempts; i++) {
    try {
      await action();
      return;
    } catch (error) {
      if (i === attempts) throw error;
    }
  }
}

await retry(async () => {
  await page.getByRole('button', { name: 'Save' }).click();
});
```

### 8.5 Function overloads (occasional, good to recognise)

```ts
function getLocator(page: Page, selector: string): Locator;
function getLocator(page: Page, selector: string, index: number): Locator;
function getLocator(page: Page, selector: string, index?: number): Locator {
  const locator = page.locator(selector);
  return index === undefined ? locator : locator.nth(index);
}
```

---

## 9. Interfaces

An interface describes the **shape** of an object. This is the workhorse of test data and API contracts.

```ts
interface Patient {
  id: number;
  firstName: string;
  lastName: string;
  nhsNumber?: string;          // optional
  readonly createdAt: string;  // cannot be reassigned
}

const patient: Patient = {
  id: 101,
  firstName: 'John',
  lastName: 'Smith',
  createdAt: '2026-01-15T09:00:00Z',
};
```

### 9.1 Extending interfaces

```ts
interface BaseUser {
  username: string;
  password: string;
}

interface AdminUser extends BaseUser {
  permissions: string[];
}

const admin: AdminUser = {
  username: 'nigel',
  password: 'secret',
  permissions: ['manage-users', 'view-audit'],
};
```

### 9.2 Interfaces for API contracts

This is where interfaces pay for themselves in an API automation suite.

```ts
interface AppointmentResponse {
  id: string;
  patientId: number;
  status: 'booked' | 'cancelled' | 'attended';
  scheduledFor: string;
  clinician: {
    id: number;
    name: string;
  };
}

const response = await request.get('/api/appointments/123');
const appointment = (await response.json()) as AppointmentResponse;

expect(appointment.status).toBe('booked');
expect(appointment.clinician.name).toBeTruthy();
// Autocomplete now works on every field, and typos are caught at compile time
```

### 9.3 Describing functions and indexes

```ts
// Callable interface
interface Formatter {
  (value: string): string;
}

// Index signature, dictionary of unknown keys
interface Headers {
  [key: string]: string;
}

const headers: Headers = {
  Authorization: 'Bearer token',
  'Content-Type': 'application/json',
};
```

### 9.4 Declaration merging (interfaces only)

Two interfaces with the same name merge. This is exactly how you extend Playwright's own types.

```ts
interface Window {
  appVersion: string;
}
interface Window {
  featureFlags: Record<string, boolean>;
}
// Window now has both properties
```

---

## 10. Type aliases

A `type` gives a name to *any* type, not just object shapes.

```ts
type Environment = 'dev' | 'qa' | 'staging' | 'prod';
type Milliseconds = number;
type UserId = string | number;

type Credentials = {
  username: string;
  password: string;
};

type LoginFn = (creds: Credentials) => Promise<void>;

type ApiResult<T> = {
  data: T;
  status: number;
};
```

Combining with intersection instead of `extends`:

```ts
type BaseUser = { username: string; password: string };
type WithRole = { role: 'admin' | 'clinician' | 'receptionist' };
type TestUser = BaseUser & WithRole;

const user: TestUser = { username: 'nigel', password: 'x', role: 'admin' };
```

---

## 11. Interface vs type alias

| | `interface` | `type` |
|---|---|---|
| Object shapes | Yes | Yes |
| Unions (`'a' \| 'b'`) | No | Yes |
| Primitives, tuples, functions | Awkward | Yes |
| Extending | `extends` | `&` intersection |
| Declaration merging | Yes | No |
| Better error messages for objects | Slightly | |

**Team convention worth adopting and writing down:**

- `interface` for object shapes: page object configs, API request and response bodies, test data models.
- `type` for everything else: unions, aliases, function signatures, mapped and utility type compositions.

Pick one convention and enforce it in review. The worst outcome is half the repo using each at random.

---

## 12. Union and intersection types

### 12.1 Union: this OR that

```ts
type Environment = 'dev' | 'qa' | 'staging' | 'prod';
type Id = string | number;

let env: Environment = 'qa';
// env = 'uat';   // Error: not assignable, typo caught instantly

function getBaseUrl(env: Environment): string {
  const urls: Record<Environment, string> = {
    dev: 'https://dev.example.com',
    qa: 'https://qa.example.com',
    staging: 'https://staging.example.com',
    prod: 'https://www.example.com',
  };
  return urls[env];
}
```

Union of object shapes, a discriminated union:

```ts
type ApiResponse =
  | { ok: true; data: Patient }
  | { ok: false; error: string };

function handle(response: ApiResponse) {
  if (response.ok) {
    console.log(response.data.firstName);  // TS knows 'data' exists here
  } else {
    console.log(response.error);           // TS knows 'error' exists here
  }
}
```

### 12.2 Intersection: this AND that

```ts
type Timestamps = { createdAt: string; updatedAt: string };
type Patient = { id: number; name: string };

type PatientRecord = Patient & Timestamps;

const record: PatientRecord = {
  id: 1,
  name: 'John Smith',
  createdAt: '2026-01-01',
  updatedAt: '2026-01-02',
};
```

**Memory hook:** union `|` gives you **fewer usable properties** (only what is common), intersection `&` gives you **more** (everything combined).

---

## 13. Literal types, narrowing and type guards

### 13.1 Literal types

```ts
type LogLevel = 'info' | 'warn' | 'error';
type Retry = 0 | 1 | 2 | 3;
type Headless = true;
```

### 13.2 Narrowing

TypeScript follows your `if` statements and narrows the type automatically.

```ts
function describe(value: string | number): string {
  if (typeof value === 'number') {
    return value.toFixed(2);      // here value is number
  }
  return value.trim();            // here value is string
}
```

Narrowing tools:

```ts
typeof value === 'string'        // primitives
Array.isArray(value)             // arrays
value instanceof Error           // classes
'name' in patient                // property presence
value !== null                   // truthiness and null checks
```

### 13.3 Custom type guards

```ts
interface Patient { id: number; nhsNumber: string; }

function isPatient(value: unknown): value is Patient {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'nhsNumber' in value
  );
}

const body: unknown = await response.json();
if (isPatient(body)) {
  expect(body.nhsNumber).toMatch(/^\d{10}$/);   // fully typed here
}
```

### 13.4 Exhaustiveness checking with `never`

Add a new status to the union and the compiler will tell you which switch statements you forgot to update. This is a genuinely great safety net in a large suite.

```ts
type Status = 'booked' | 'cancelled' | 'attended';

function label(status: Status): string {
  switch (status) {
    case 'booked': return 'Booked';
    case 'cancelled': return 'Cancelled';
    case 'attended': return 'Attended';
    default: {
      const exhaustive: never = status;
      throw new Error(`Unhandled status: ${exhaustive}`);
    }
  }
}
```

---

## 14. Enums

An enum is a named set of constants.

```ts
enum UserRole {
  Admin = 'ADMIN',
  Clinician = 'CLINICIAN',
  Receptionist = 'RECEPTIONIST',
}

const role: UserRole = UserRole.Admin;
console.log(role);   // 'ADMIN'
```

Numeric enums auto increment, which is usually not what you want in test data because the compiled value is meaningless in a log.

```ts
enum Priority { Low, Medium, High }   // 0, 1, 2
console.log(Priority.High);           // 2, not very helpful in a report
```

### 14.1 The modern alternative: const object plus union

Enums are the one TypeScript feature that generates real JavaScript at runtime, and they interact awkwardly with `isolatedModules` and some bundlers. Most modern codebases prefer this:

```ts
export const UserRole = {
  Admin: 'ADMIN',
  Clinician: 'CLINICIAN',
  Receptionist: 'RECEPTIONIST',
} as const;

export type UserRole = (typeof UserRole)[keyof typeof UserRole];
// UserRole is now 'ADMIN' | 'CLINICIAN' | 'RECEPTIONIST'

function loginAs(role: UserRole) { /* ... */ }

loginAs(UserRole.Admin);   // works
loginAs('CLINICIAN');      // also works, plain strings are allowed
// loginAs('DOCTOR');      // Error, typo caught
```

**Practical guidance for a QE team:** use `const` objects plus a union type for test data and roles. Reach for a real `enum` only when you have an existing convention to match.

---

## 15. Classes and the Page Object Model

This is where TypeScript starts to feel familiar if you come from Java and Selenide.

### 15.1 Class basics

```ts
class TestUser {
  // Properties with visibility modifiers
  public readonly username: string;
  private password: string;
  protected role: string;

  constructor(username: string, password: string, role = 'clinician') {
    this.username = username;
    this.password = password;
    this.role = role;
  }

  // Method
  public masked(): string {
    return `${this.username} / ${'*'.repeat(this.password.length)}`;
  }

  // Getter
  get isAdmin(): boolean {
    return this.role === 'admin';
  }

  // Static factory method
  static admin(): TestUser {
    return new TestUser('nigel', 'secret', 'admin');
  }
}

const user = TestUser.admin();
console.log(user.isAdmin);   // true, note: no parentheses on a getter
```

**Visibility modifiers:**

| Modifier | Meaning |
|---|---|
| `public` | Default, accessible everywhere |
| `private` | Only inside this class |
| `protected` | This class and subclasses |
| `readonly` | Assignable only in the constructor |

**Parameter properties shorthand** (very common in page objects):

```ts
class LoginPage {
  constructor(private readonly page: Page) {}
  // Declares AND assigns this.page in one line, no boilerplate
}
```

### 15.2 A real Playwright page object

```ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  private readonly usernameInput: Locator;
  private readonly passwordInput: Locator;
  private readonly signInButton: Locator;
  private readonly errorMessage: Locator;

  constructor(private readonly page: Page) {
    this.usernameInput = page.getByLabel('Username');
    this.passwordInput = page.getByLabel('Password');
    this.signInButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto(): Promise<void> {
    await this.page.goto('/login');
  }

  async login(username: string, password: string): Promise<void> {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.signInButton.click();
  }

  async expectErrorMessage(expected: string | RegExp): Promise<void> {
    await expect(this.errorMessage).toHaveText(expected);
  }
}
```

Notice: locators are **defined** in the constructor but not **resolved** there. Playwright locators are lazy, so this is safe and is the recommended pattern.

### 15.3 Inheritance with a BasePage

```ts
export abstract class BasePage {
  protected constructor(protected readonly page: Page) {}

  abstract get path(): string;          // every subclass must provide this

  async goto(): Promise<void> {
    await this.page.goto(this.path);
  }

  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }
}

export class DashboardPage extends BasePage {
  private readonly welcomeBanner: Locator;

  constructor(page: Page) {
    super(page);                        // must call super() first
    this.welcomeBanner = page.getByTestId('welcome-banner');
  }

  get path(): string {
    return '/dashboard';
  }

  async expectWelcome(name: string): Promise<void> {
    await expect(this.welcomeBanner).toContainText(name);
  }
}
```

### 15.4 Implementing an interface

```ts
interface Navigable {
  goto(): Promise<void>;
  isLoaded(): Promise<boolean>;
}

export class PatientListPage implements Navigable {
  constructor(private readonly page: Page) {}

  async goto(): Promise<void> {
    await this.page.goto('/patients');
  }

  async isLoaded(): Promise<boolean> {
    return this.page.getByRole('heading', { name: 'Patients' }).isVisible();
  }
}
```

If you forget `isLoaded`, the compiler fails the build. This is a genuinely useful contract when seven engineers are adding page objects to the same repo.

**Pitfall:** never store `await`ed element state as a class field. Store `Locator` objects, which are lazy and re-resolve on every action. Storing a resolved `ElementHandle` is the number one cause of stale element style flakiness in Playwright.

---

## 16. Generics

A generic is a **type parameter**: a placeholder for a type that the caller supplies. If you have used `List<String>` in Java, you already understand this.

### 16.1 The problem generics solve

```ts
// Without generics, you lose the type
function firstAny(items: any[]): any {
  return items[0];
}
const name = firstAny(['nigel', 'ravindu']);   // type is any, no autocomplete

// With generics, the type flows through
function first<T>(items: T[]): T | undefined {
  return items[0];
}
const name2 = first(['nigel', 'ravindu']);     // type is string
const id = first([1, 2, 3]);                   // type is number
```

`T` is just a convention. `T` for type, `K` for key, `V` for value, `R` for return. Name it meaningfully when it helps.

### 16.2 Generic API client, the killer use case in test automation

```ts
import { APIRequestContext } from '@playwright/test';

export class ApiClient {
  constructor(private readonly request: APIRequestContext) {}

  async get<T>(url: string): Promise<T> {
    const response = await this.request.get(url);
    if (!response.ok()) {
      throw new Error(`GET ${url} failed with ${response.status()}`);
    }
    return (await response.json()) as T;
  }

  async post<TBody, TResponse>(url: string, body: TBody): Promise<TResponse> {
    const response = await this.request.post(url, { data: body });
    return (await response.json()) as TResponse;
  }
}

// Usage: fully typed responses, autocomplete on every field
interface Patient { id: number; firstName: string; nhsNumber: string; }
interface CreatePatientRequest { firstName: string; lastName: string; }

const api = new ApiClient(request);
const patient = await api.get<Patient>('/api/patients/101');
expect(patient.nhsNumber).toMatch(/^\d{10}$/);

const created = await api.post<CreatePatientRequest, Patient>('/api/patients', {
  firstName: 'John',
  lastName: 'Smith',
});
```

### 16.3 Constraints with `extends`

Restrict what types are allowed.

```ts
// T must have an 'id' property
function findById<T extends { id: number }>(items: T[], id: number): T | undefined {
  return items.find(item => item.id === id);
}

// K must be a key of T
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map(item => item[key]);
}

const patients = [{ id: 1, name: 'John' }, { id: 2, name: 'Jane' }];
const names = pluck(patients, 'name');   // string[]
// pluck(patients, 'age');               // Error: 'age' is not a key
```

### 16.4 Default type parameters

```ts
interface TestData<T = Record<string, string>> {
  name: string;
  payload: T;
}

const simple: TestData = { name: 'basic', payload: { key: 'value' } };
const typed: TestData<Patient> = { name: 'patient', payload: patientFixture };
```

### 16.5 A generic test data builder

Useful for a shared framework utility.

```ts
export class Builder<T extends object> {
  private data: Partial<T> = {};

  with<K extends keyof T>(key: K, value: T[K]): this {
    this.data[key] = value;
    return this;                       // enables method chaining
  }

  build(defaults: T): T {
    return { ...defaults, ...this.data };
  }
}

const patient = new Builder<Patient>()
  .with('firstName', 'Override')
  .build({ id: 1, firstName: 'John', nhsNumber: '1234567890' });
```

---

## 17. Type assertions

You are telling the compiler "trust me, I know what this is". The compiler does not verify it, so an incorrect assertion is a runtime bug waiting to happen.

```ts
const body = (await response.json()) as Patient;

// Alternative angle bracket syntax, do NOT use it in .tsx files
const body2 = <Patient>await response.json();
```

### 17.1 Non null assertion `!`

```ts
const text = await page.locator('h1').textContent();
console.log(text!.toUpperCase());   // "I promise this is not null"
```

`!` is fast but risky. In a test, prefer a real assertion that produces a meaningful failure message:

```ts
// Better: fails with a clear message instead of "cannot read property of null"
await expect(page.locator('h1')).toHaveText('Dashboard');

// Or narrow explicitly
const text = await page.locator('h1').textContent();
expect(text).not.toBeNull();
console.log(text?.toUpperCase());
```

### 17.2 `as const`

Freezes a value into its narrowest literal type. Extremely handy for test data tables.

```ts
const roles = ['admin', 'clinician'] as const;
// type is readonly ['admin', 'clinician'], not string[]

type Role = (typeof roles)[number];   // 'admin' | 'clinician'

const config = {
  env: 'qa',
  retries: 2,
} as const;
// config.env is exactly 'qa', and every property is readonly
```

### 17.3 `satisfies`, the modern alternative to `as`

`satisfies` checks the value against a type **without widening it**. You get validation and precise inference at the same time.

```ts
type EnvUrls = Record<string, string>;

const urls = {
  dev: 'https://dev.example.com',
  qa: 'https://qa.example.com',
} satisfies EnvUrls;

urls.qa.toUpperCase();   // string methods available, keys are still exactly 'dev' | 'qa'
// urls.prod;            // Error: property does not exist, caught at compile time
```

**Rule:** prefer `satisfies` over `as` whenever you are describing a literal you wrote yourself. Save `as` for data coming from outside your program.

---

## 18. Optional chaining and nullish coalescing

### 18.1 Optional chaining `?.`

Short circuits to `undefined` instead of throwing when something in the chain is null or undefined.

```ts
const clinicianName = appointment?.clinician?.name;         // undefined if any step is missing

const count = response?.data?.items?.length ?? 0;

// Optional call, only calls if the function exists
onComplete?.();

// Optional index access
const firstError = errors?.[0];
```

### 18.2 Nullish coalescing `??`

Falls back **only** when the left side is `null` or `undefined`.

```ts
const timeout = process.env.TIMEOUT ?? '30000';
const retries = config.retries ?? 2;
```

### 18.3 `??` versus `||`, the difference that bites people

`||` falls back on any falsy value: `0`, `''`, `false`, `NaN`, `null`, `undefined`.
`??` falls back only on `null` and `undefined`.

```ts
const retries1 = 0 || 3;    // 3   WRONG, zero retries was intentional
const retries2 = 0 ?? 3;    // 0   CORRECT

const headless1 = false || true;   // true   WRONG
const headless2 = false ?? true;   // false  CORRECT

const name1 = '' || 'default';     // 'default'
const name2 = '' ?? 'default';     // ''
```

**Rule for config code:** always use `??` unless you specifically want empty string and zero to trigger the fallback.

### 18.4 Nullish assignment `??=`

```ts
let baseUrl: string | undefined;
baseUrl ??= 'https://qa.example.com';   // assigns only if null or undefined
```

---

## 19. Modules: import and export

Every `.ts` file with an `import` or `export` is a module with its own scope.

### 19.1 Named exports, the default choice for a framework

```ts
// utils/data-helper.ts
export const DEFAULT_TIMEOUT = 30_000;

export function randomNhsNumber(): string {
  return String(Math.floor(1_000_000_000 + Math.random() * 9_000_000_000));
}

export interface Patient {
  id: number;
  firstName: string;
}
```

```ts
// tests/patient.spec.ts
import { DEFAULT_TIMEOUT, randomNhsNumber, type Patient } from '../utils/data-helper';
```

### 19.2 Default exports (use sparingly)

```ts
// pages/login.page.ts
export default class LoginPage { /* ... */ }

// consumer
import LoginPage from '../pages/login.page';   // name is arbitrary, easy to make inconsistent
```

Named exports refactor better and keep imports consistent across a team. Prefer them.

### 19.3 Renaming, namespace imports and re-exports

```ts
import { LoginPage as SignInPage } from './pages/login.page';
import * as testData from './fixtures/patients';

// pages/index.ts, a barrel file
export * from './login.page';
export * from './dashboard.page';

// consumers get one clean import
import { LoginPage, DashboardPage } from '../pages';
```

### 19.4 Type only imports

Signals that the import disappears at compile time. Required when `isolatedModules` or `verbatimModuleSyntax` is on.

```ts
import type { Page, Locator } from '@playwright/test';
import { expect, type APIRequestContext } from '@playwright/test';
```

### 19.5 Path aliases

Kill the `../../../..` chains. Configure once in `tsconfig.json`:

```jsonc
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@pages/*": ["src/pages/*"],
      "@fixtures/*": ["src/fixtures/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

```ts
import { LoginPage } from '@pages/login.page';
```

---

## 20. Utility types

Built in generics that transform existing types. These stop you duplicating interfaces.

Assume this base type for every example:

```ts
interface Patient {
  id: number;
  firstName: string;
  lastName: string;
  nhsNumber: string;
  active: boolean;
}
```

| Utility | What it does | Example |
|---|---|---|
| `Partial<T>` | All properties optional | `Partial<Patient>` |
| `Required<T>` | All properties required | `Required<Patient>` |
| `Readonly<T>` | All properties readonly | `Readonly<Patient>` |
| `Pick<T, K>` | Keep only these keys | `Pick<Patient, 'id' \| 'nhsNumber'>` |
| `Omit<T, K>` | Remove these keys | `Omit<Patient, 'id'>` |
| `Record<K, V>` | Build a dictionary | `Record<Environment, string>` |
| `Exclude<T, U>` | Remove members from a union | `Exclude<Role, 'admin'>` |
| `Extract<T, U>` | Keep matching union members | `Extract<Status, 'booked'>` |
| `NonNullable<T>` | Strip null and undefined | `NonNullable<string \| null>` |
| `ReturnType<F>` | The return type of a function | `ReturnType<typeof buildUrl>` |
| `Parameters<F>` | Tuple of parameter types | `Parameters<typeof login>` |
| `Awaited<T>` | Unwrap a Promise | `Awaited<Promise<Patient>>` |
| `keyof T` | Union of the keys | `keyof Patient` |
| `typeof x` | The type of a value | `typeof config` |

### Worked examples

```ts
// Partial: an override object for a test data builder
function buildPatient(overrides: Partial<Patient> = {}): Patient {
  return {
    id: 1,
    firstName: 'John',
    lastName: 'Smith',
    nhsNumber: '1234567890',
    active: true,
    ...overrides,
  };
}
const inactive = buildPatient({ active: false });

// Omit: a create request has no server generated id
type CreatePatientRequest = Omit<Patient, 'id'>;

// Pick: a lightweight summary used in a list assertion
type PatientSummary = Pick<Patient, 'id' | 'firstName' | 'lastName'>;

// Record: an environment to URL map, compiler enforces every env is present
type Environment = 'dev' | 'qa' | 'prod';
const urls: Record<Environment, string> = {
  dev: 'https://dev.example.com',
  qa: 'https://qa.example.com',
  prod: 'https://www.example.com',
};

// keyof: a type safe field name
type PatientField = keyof Patient;   // 'id' | 'firstName' | 'lastName' | 'nhsNumber' | 'active'

// ReturnType and Awaited: derive a type instead of writing it twice
async function fetchPatient(id: number): Promise<Patient> { /* ... */ }
type FetchedPatient = Awaited<ReturnType<typeof fetchPatient>>;   // Patient

// typeof on a config object, single source of truth
const testConfig = {
  baseUrl: 'https://qa.example.com',
  retries: 2,
  headless: true,
};
type TestConfig = typeof testConfig;
```

**Why this matters at scale:** derive types from one source rather than maintaining five near identical interfaces. When the API adds a field, you change one interface and everything downstream updates.

---

## 21. Async, await and Promises

Almost every Playwright call is asynchronous. Getting this right is the difference between a stable suite and a flaky one.

```ts
// An async function ALWAYS returns a Promise
async function getTitle(page: Page): Promise<string> {
  return page.title();     // returning string is fine, TS wraps it
}

// await unwraps the Promise
const title = await getTitle(page);   // string, not Promise<string>
```

### 21.1 The missing await bug

```ts
// BROKEN: click is never awaited, the test races ahead
test('save record', async ({ page }) => {
  page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Saved')).toBeVisible();
});

// CORRECT
test('save record', async ({ page }) => {
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Saved')).toBeVisible();
});
```

TypeScript will not catch this on its own. Turn on the ESLint rule:

```jsonc
// eslint.config.js rules
"@typescript-eslint/no-floating-promises": "error",
"@typescript-eslint/await-thenable": "error"
```

This one rule pair eliminates an entire category of flakiness. Add it to your shared config today.

### 21.2 Parallel awaits

```ts
// Sequential, slow
const title = await page.title();
const url = page.url();

// Parallel, when the calls are independent
const [patients, appointments] = await Promise.all([
  api.get<Patient[]>('/api/patients'),
  api.get<Appointment[]>('/api/appointments'),
]);
```

`Promise.all` rejects as soon as any one fails. Use `Promise.allSettled` when you want every result regardless.

### 21.3 Error handling and typed catches

Under `useUnknownInCatchVariables` (part of `strict`), the caught error is `unknown`.

```ts
try {
  await api.get<Patient>('/api/patients/999');
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Request failed: ${message}`);
  throw error;
}
```

**Pitfall:** never wrap a Playwright `expect` in try/catch to "handle" the failure. That silently converts a real failure into a pass. Use `expect.soft()` if you want the test to continue after a non blocking assertion.

---

## 22. Modern JavaScript essentials you will use daily

### 22.1 Template literals

```ts
const env = 'qa';
const url = `https://${env}.example.com/patients?active=true`;

const multiline = `
  Test: ${testName}
  Duration: ${duration}ms
`;
```

Template literal **types** are a bonus:

```ts
type Env = 'dev' | 'qa';
type BaseUrl = `https://${Env}.example.com`;   // 'https://dev.example.com' | 'https://qa.example.com'
```

### 22.2 Destructuring

```ts
const { firstName, nhsNumber } = patient;
const { firstName: name = 'Unknown' } = patient;    // rename plus default
const [first, second] = usernames;
const { clinician: { name: clinicianName } } = appointment;   // nested

// The Playwright fixture pattern is just destructuring
test('example', async ({ page, request, browserName }) => { /* ... */ });
```

### 22.3 Spread and rest

```ts
const defaults = { retries: 2, timeout: 30_000 };
const options = { ...defaults, timeout: 60_000 };   // later keys win

const allUsers = [...admins, ...clinicians];

const { id, ...withoutId } = patient;               // rest in destructuring
```

**Careful:** spread is a shallow copy. Nested objects are still shared by reference.

```ts
const copy = { ...config };
copy.auth.username = 'changed';   // this ALSO changes config.auth.username

const deepCopy = structuredClone(config);   // Node 17+, real deep copy
```

### 22.4 Arrow functions and `this`

```ts
const isActive = (p: Patient): boolean => p.active;

// Arrow functions inherit 'this' from the enclosing scope.
// Regular functions do not, which is why callbacks in classes usually use arrows.
```

### 22.5 Optional string and array helpers you will reach for

```ts
'ORD-123'.startsWith('ORD-');
'  text '.trim();
'a,b,c'.split(',');
'John Smith'.replace(/\s+/g, '-');
'abc'.includes('b');
[1, 2, 3].includes(2);
Object.keys(patient);
Object.entries(patient).forEach(([key, value]) => console.log(key, value));
```

---

## 23. tsconfig.json explained

A solid starting point for a Playwright framework:

```jsonc
{
  "compilerOptions": {
    /* Language and environment */
    "target": "ES2022",              // JS version to compile down to
    "lib": ["ES2022", "DOM"],        // DOM needed for page.evaluate() code
    "module": "CommonJS",            // Playwright's default, use NodeNext for ESM
    "moduleResolution": "node",

    /* Type safety, the part that actually matters */
    "strict": true,                  // turns on the whole strict family, keep this ON
    "noUnusedLocals": true,          // dead variables become build errors
    "noUnusedParameters": true,
    "noImplicitReturns": true,       // every code path must return
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true, // arr[0] becomes T | undefined, very strict but correct
    "forceConsistentCasingInFileNames": true,

    /* Emit */
    "noEmit": true,                  // Playwright transpiles, tsc only type checks
    "sourceMap": true,               // readable stack traces
    "skipLibCheck": true,            // skip type checking node_modules, big speed win
    "esModuleInterop": true,
    "resolveJsonModule": true,       // allows import data from './data.json'

    /* Paths */
    "baseUrl": ".",
    "paths": {
      "@pages/*": ["src/pages/*"],
      "@fixtures/*": ["src/fixtures/*"],
      "@utils/*": ["src/utils/*"]
    },

    "types": ["node"]
  },
  "include": ["src/**/*.ts", "tests/**/*.ts", "playwright.config.ts"],
  "exclude": ["node_modules", "test-results", "playwright-report", "dist"]
}
```

### What `strict: true` actually enables

| Flag | Effect |
|---|---|
| `strictNullChecks` | `null` and `undefined` must be handled explicitly |
| `noImplicitAny` | Untyped parameters are an error |
| `strictFunctionTypes` | Stricter function assignability |
| `strictBindCallApply` | Type checks `bind`, `call`, `apply` |
| `strictPropertyInitialization` | Class fields must be assigned |
| `noImplicitThis` | `this` cannot be implicitly `any` |
| `useUnknownInCatchVariables` | `catch (e)` gives `unknown`, not `any` |
| `alwaysStrict` | Emits `"use strict"` |

**Migrating an existing JavaScript suite?** Start with `strict: false`, add `"allowJs": true` and `"checkJs": false`, convert file by file, then flip `strict` on once the noise is manageable. Do not try to convert everything in one pull request.

---

## 24. Typing test data, JSON and environment variables

### 24.1 JSON test data

```jsonc
// fixtures/patients.json
[
  { "id": 1, "firstName": "John", "lastName": "Smith", "nhsNumber": "1234567890", "active": true }
]
```

```ts
// With "resolveJsonModule": true
import patientsJson from '../fixtures/patients.json';

const patients: Patient[] = patientsJson;   // validated against your interface at compile time
```

### 24.2 Environment variables are always `string | undefined`

```ts
// process.env.BASE_URL is string | undefined, ALWAYS
const baseUrl = process.env.BASE_URL ?? 'https://qa.example.com';
const retries = Number(process.env.RETRIES ?? 2);
const headless = process.env.HEADLESS !== 'false';

// Fail fast on required secrets, far better than a confusing 401 later
function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

const apiToken = requireEnv('API_TOKEN');
```

### 24.3 Declaring your own env types

```ts
// types/env.d.ts
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      BASE_URL?: string;
      API_TOKEN?: string;
      ENVIRONMENT?: 'dev' | 'qa' | 'staging' | 'prod';
    }
  }
}
export {};
```

Now `process.env.ENVIRONMNET` (typo) is a compile error, and `process.env.ENVIRONMENT` autocompletes its allowed values.

### 24.4 A typed config module

```ts
// config/test-config.ts
export interface TestConfig {
  baseUrl: string;
  apiUrl: string;
  timeout: number;
  retries: number;
}

const environments = {
  dev:  { baseUrl: 'https://dev.example.com',  apiUrl: 'https://dev-api.example.com' },
  qa:   { baseUrl: 'https://qa.example.com',   apiUrl: 'https://qa-api.example.com' },
  prod: { baseUrl: 'https://www.example.com',  apiUrl: 'https://api.example.com' },
} as const;

export type Environment = keyof typeof environments;

export function getConfig(env: Environment = 'qa'): TestConfig {
  return {
    ...environments[env],
    timeout: Number(process.env.TIMEOUT ?? 30_000),
    retries: Number(process.env.RETRIES ?? 1),
  };
}
```

---

## 25. Playwright specific TypeScript patterns

### 25.1 The core types you will import

```ts
import {
  test,
  expect,
  type Page,             // the browser tab
  type Locator,          // a lazy element reference
  type BrowserContext,   // an isolated session
  type APIRequestContext,// the API client
  type APIResponse,
  type TestInfo,         // metadata about the running test
} from '@playwright/test';
```

### 25.2 Typed custom fixtures, the pattern that makes POM clean

```ts
// fixtures/test-fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '@pages/login.page';
import { DashboardPage } from '@pages/dashboard.page';

type Pages = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
};

type WorkerFixtures = {
  apiToken: string;
};

export const test = base.extend<Pages, WorkerFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },

  apiToken: [
    async ({}, use) => {
      const token = await fetchToken();
      await use(token);
    },
    { scope: 'worker' },   // created once per worker, not per test
  ],
});

export { expect } from '@playwright/test';
```

```ts
// tests/login.spec.ts
import { test, expect } from '@fixtures/test-fixtures';

test('valid user reaches the dashboard', async ({ loginPage, dashboardPage }) => {
  await loginPage.goto();
  await loginPage.login('nigel', 'Passw0rd!');
  await dashboardPage.expectWelcome('Nigel');
});
```

Every fixture is fully typed and autocompletes in the destructured parameter list. New engineers discover the available page objects just by typing `{`.

### 25.3 Typed data driven tests

```ts
interface LoginCase {
  description: string;
  username: string;
  password: string;
  expectedError: string | RegExp;
}

const invalidLogins: LoginCase[] = [
  { description: 'empty password', username: 'nigel', password: '', expectedError: 'Password is required' },
  { description: 'unknown user', username: 'ghost', password: 'x', expectedError: /invalid credentials/i },
  { description: 'locked account', username: 'locked', password: 'x', expectedError: 'Account locked' },
];

for (const testCase of invalidLogins) {
  test(`login fails: ${testCase.description}`, async ({ loginPage }) => {
    await loginPage.goto();
    await loginPage.login(testCase.username, testCase.password);
    await loginPage.expectErrorMessage(testCase.expectedError);
  });
}
```

Add a field to `LoginCase` and the compiler lists every case you have not updated. That is exactly the maintainability property you want when the suite has 400 tests.

### 25.4 Typing `page.evaluate`

Code inside `evaluate` runs in the browser, not in Node. Types do not automatically cross that boundary.

```ts
// Explicit return type
const version = await page.evaluate<string>(() => window.document.title);

// Passing an argument in, note the single argument rule
const height = await page.evaluate((selector: string) => {
  return document.querySelector(selector)?.clientHeight ?? 0;
}, '#main');

// Declaring a custom window property
declare global {
  interface Window {
    appVersion?: string;
  }
}
const appVersion = await page.evaluate(() => window.appVersion);
```

### 25.5 Typed API response assertions

```ts
interface ErrorResponse {
  code: string;
  message: string;
  details?: string[];
}

test('rejects invalid NHS number', async ({ request }) => {
  const response = await request.post('/api/patients', {
    data: { firstName: 'John', nhsNumber: 'abc' },
  });

  expect(response.status()).toBe(400);

  const body = (await response.json()) as ErrorResponse;
  expect(body.code).toBe('INVALID_NHS_NUMBER');
  expect(body.details ?? []).toContain('nhsNumber must be 10 digits');
});
```

### 25.6 A typed custom matcher

```ts
import { expect as baseExpect } from '@playwright/test';

export const expect = baseExpect.extend({
  async toBeValidNhsNumber(received: string) {
    const pass = /^\d{10}$/.test(received);
    return {
      pass,
      message: () => `Expected ${received} ${pass ? 'not ' : ''}to be a 10 digit NHS number`,
    };
  },
});

// Usage, fully typed
await expect(patient.nhsNumber).toBeValidNhsNumber();
```

---

## 26. Common compiler errors and how to fix them

| Error | Meaning | Fix |
|---|---|---|
| `Object is possibly 'null'` | Value can be null under strict mode | Use `?.`, a null check, or a Playwright `expect` |
| `Object is possibly 'undefined'` | Optional value or `noUncheckedIndexedAccess` | Use `??`, a guard, or `array.at(0)` with a check |
| `Property 'x' does not exist on type 'y'` | Typo, or the interface is missing a field | Fix the typo or update the interface |
| `Type 'string' is not assignable to type '"qa" \| "dev"'` | Value outside the union | Use a union member, or widen the type |
| `Parameter 'x' implicitly has an 'any' type` | Missing annotation | Annotate the parameter |
| `Cannot find module '@pages/login.page'` | Path alias not configured or not resolved at runtime | Check `tsconfig.json` `paths`, and that Playwright resolves them |
| `Argument of type 'Promise<string>' is not assignable to 'string'` | Missing `await` | Add `await` |
| `'error' is of type 'unknown'` | Strict catch variables | `error instanceof Error ? error.message : String(error)` |
| `Property has no initializer and is not definitely assigned` | `strictPropertyInitialization` | Assign in the constructor, give a default, or mark optional |
| `Type 'X' is missing the following properties` | Object does not match the interface | Add the missing fields, or use `Partial<X>` |

**Reading a TypeScript error:** read it from the **bottom up**. The last line is usually the actual mismatch. The lines above are the chain of how it got there.

---

## 27. Best practices

### Type safety

1. Turn `strict: true` on from day one. Retrofitting it into a mature suite is painful.
2. Ban `any`. Use `unknown` at trust boundaries and narrow it.
3. Prefer `satisfies` over `as` for values you author yourself.
4. Model API contracts as interfaces. They double as living documentation of the API your team tests.
5. Do not annotate what is inferred. Annotate function parameters, function return types on exported functions, and empty collections.

### Framework architecture

6. Page Object Model by default. One class per page or component, private locators, public intent revealing methods.
7. Store `Locator` objects, never resolved `ElementHandle` objects.
8. Page objects return data or `void`, they should not contain assertions unless the method name says so (`expectErrorMessage`).
9. Use custom fixtures for page object instantiation. Never call `new LoginPage(page)` inside a test body.
10. Named exports over default exports. Barrel files for clean imports.
11. Put shared types in a `types/` folder or next to the module that owns them, and export them.

### Test code quality

12. Web first assertions only: `await expect(locator).toBeVisible()`, never `await page.waitForTimeout(3000)`.
13. Enable `@typescript-eslint/no-floating-promises`. Missing `await` is the most common source of flakiness in a TypeScript suite.
14. Prefer `??` over `||` for defaults in config code.
15. Type your test data. `Patient[]` catches malformed fixtures at build time instead of at 2 am in a nightly run.
16. Run `tsc --noEmit` as a dedicated CI stage. Playwright will not fail your build on a type error by itself.

### Team scale

17. Write down your `interface` versus `type` convention, your naming convention, and your folder structure. Enforce them with ESLint where possible, in review where not.
18. Any rule that can be automated should be a lint rule, not a review comment. Reviewer time is expensive.
19. Keep a shared `tsconfig.base.json` if you have multiple product repos, so standards do not drift per project.

### Suggested folder structure

```
src/
  pages/          LoginPage, DashboardPage, one class per page
  components/     shared UI components: DatePicker, Modal, DataGrid
  fixtures/       custom Playwright fixtures and test data
  api/            typed API clients
  utils/          helpers: date, random data, file handling
  types/          shared interfaces and type aliases
  config/         environment configuration
tests/
  ui/
  api/
  accessibility/
playwright.config.ts
tsconfig.json
eslint.config.js
```

---

## 28. Common pitfalls

| Pitfall | Why it hurts | Do this instead |
|---|---|---|
| Missing `await` | Test races ahead, random failures | Enable `no-floating-promises` |
| `any` sprinkled everywhere | Type checking silently disabled | `unknown` plus narrowing |
| `!` non null assertion in tests | Failure message is useless | Use `expect(...)` to assert, then use the value |
| `||` for defaults | `0` and `false` get overwritten | Use `??` |
| Storing `ElementHandle` in a class | Stale element flakiness | Store `Locator`, it re-resolves |
| Assertions inside generic page methods | Page objects become untestable and rigid | Return state, assert in the test |
| `as` used to silence a compiler error | You lied to the compiler, bug ships | Fix the type, or narrow properly |
| Shallow spread on nested config | Two objects share nested state | `structuredClone` for deep copies |
| Numeric enums in test data | Logs show `2` instead of `HIGH` | String enums or `const` object plus union |
| No `tsc --noEmit` in CI | Type errors reach main | Add a dedicated type check job |
| Giant `utils.ts` with 40 exports | Nobody can find anything | Split by concern: `date.util.ts`, `data.util.ts` |
| `Promise.all` on dependent steps | Race conditions in the UI | Only parallelise genuinely independent work |

---

## 29. Practice exercises

Good starter tasks for a manual tester learning TypeScript. Roughly in order of difficulty.

1. **Types:** declare a `TestEnvironment` union of `'dev' | 'qa' | 'staging' | 'prod'` and a `Record` mapping each to a base URL. Make an invalid key fail to compile.
2. **Interfaces:** model a real API response from your product as an interface, including at least one optional field and one nested object.
3. **Functions:** write `buildQueryString(params: Record<string, string | number | boolean>): string` that turns an object into `?a=1&b=true`.
4. **Optional chaining:** given `response?.data?.items`, safely return the count with a fallback of zero.
5. **Classes:** convert an existing test file of yours into a page object with private locators and public methods.
6. **Generics:** write `groupBy<T, K extends keyof T>(items: T[], key: K): Record<string, T[]>`.
7. **Utility types:** given a `Patient` interface, derive `CreatePatientRequest` (no `id`) and `PatientSummary` (only `id`, `firstName`, `lastName`) without retyping fields.
8. **Type guards:** write `isErrorResponse(value: unknown): value is ErrorResponse` and use it after a `request.post`.
9. **Fixtures:** build a typed custom fixture that logs in as an admin and exposes an authenticated `page`.
10. **Exhaustiveness:** write a `switch` over an appointment status union with a `never` default, then add a new status and watch the compiler point at the gap.

---

## 30. One page summary

### Syntax cheat card

```ts
// Types
let s: string; let n: number; let b: boolean;
let arr: string[]; let tup: [number, string];
let u: string | number;              // union
let i: TypeA & TypeB;                // intersection
let anyVal: unknown;                 // safe any

// Shapes
interface User { id: number; name?: string; readonly created: string; }
type Env = 'dev' | 'qa' | 'prod';

// Functions
function f(a: string, b = 2, ...rest: number[]): string { return a; }
const g = async (p: Page): Promise<string> => p.title();

// Classes
class Page1 {
  constructor(private readonly page: Page) {}
  async goto(): Promise<void> { await this.page.goto('/'); }
}

// Generics
function first<T>(items: T[]): T | undefined { return items[0]; }
async function get<T>(url: string): Promise<T> { /* ... */ }

// Safety operators
value?.prop?.[0]?.();                // optional chaining
value ?? 'fallback';                 // nullish coalescing
value as User;                       // assertion, use sparingly
{ a: 1 } satisfies Config;           // validated, not widened
[1, 2] as const;                     // literal, readonly

// Utility types
Partial<T> Required<T> Readonly<T> Pick<T,K> Omit<T,K>
Record<K,V> Exclude<T,U> Extract<T,U> NonNullable<T>
ReturnType<F> Parameters<F> Awaited<T> keyof T typeof x

// Modules
export const x = 1;  export interface Y {}
import { x, type Y } from './module';
```

### The ten things that matter most

1. Types exist at compile time only. They cannot validate runtime data for you.
2. `strict: true` is where all the value is. Turn it on.
3. Let TypeScript infer. Annotate parameters and exported return types.
4. `interface` for object shapes, `type` for unions and everything else.
5. Union `|` narrows what you can use, intersection `&` widens it.
6. `unknown` instead of `any`, then narrow with a type guard.
7. `??` not `||` for defaults. `?.` for safe access.
8. Generics carry types through helpers. A generic API client is the single highest value pattern in an automation framework.
9. Utility types stop you duplicating interfaces. Derive, do not copy.
10. Missing `await` is the number one flakiness cause. Lint for it.

### Learning path for a manual tester joining the team

| Week | Focus |
|---|---|
| 1 | Sections 1 to 8: types, inference, arrays, objects, functions |
| 2 | Sections 9 to 14: interfaces, type aliases, unions, narrowing, enums |
| 3 | Section 15 and 25: classes, POM, Playwright fixtures. Write a real page object |
| 4 | Sections 16 to 21: generics, assertions, modules, utility types, async |
| 5 | Sections 22 to 24 and 27: tsconfig, config typing, best practices. Review a teammate's PR |

### Further reading

- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/intro.html
- TypeScript Playground (run TS in the browser): https://www.typescriptlang.org/play
- Playwright TypeScript docs: https://playwright.dev/docs/test-typescript
- typescript-eslint rules: https://typescript-eslint.io/rules/

---

*Reference document for QE onboarding and the Test Automation Knowledge Group. Examples target Playwright with TypeScript, Node 20+, strict mode enabled.*
