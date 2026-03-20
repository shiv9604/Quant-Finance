### C++ Foundations - Program Entry & Boilerplate

C++ programs are compiled native executables. Unlike interpreted languages, C++ code is compiled ahead of time into machine instructions and executed directly by the operating system.

A minimal valid C++ program:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello World\n";
    return 0;
}
```

**Compilation Model -**
1. C++ programs go through three stages:
   - Preprocessor.
   - Compiler.
   - Linker.
2. The preprocessor handles directives like `#include`.
3. The compiler converts source code into object code.
4. The linker connects object code with standard libraries.
5. Final output is a native executable binary.

**Preprocessor Directive — `#include` -**
1. `#include` tells the preprocessor to copy contents of a header file into the program.
2. `<iostream>` is a standard library header.
3. Angle brackets `< >` indicate standard library files.
4. Double quotes `" "` indicate local project files.
5. Without including `iostream`, `std::cout` would be undefined.

**Program Entry Point — `main()` -**
1. Every C++ program must contain exactly one `main()` function.
2. The operating system calls `main()` when execution begins.
3. Execution always starts inside `main`.
4. The function body is enclosed within `{ }`.

**Return Type — `int` -**
1. `int` specifies that `main` returns an integer.
2. The returned integer is called the exit status code.
3. `return 0;` indicates successful execution.
4. Any non-zero return value indicates abnormal termination by convention.
5. The exit code is consumed by:
   - Operating system.
   - Shell scripts.
   - Process managers.
   - Docker / Kubernetes.
   - Monitoring systems.

**Scope Braces `{ }` -**
1. Curly braces define the function body.
2. All executable statements must be inside these braces.
3. Variables declared inside are scoped to the function.
4. When the closing brace is reached, execution of the function ends.

**Standard Namespace — `std` -**
1. `std` stands for standard namespace.
2. It contains components from the C++ Standard Library.
3. Namespaces prevent naming conflicts in large systems.
4. Accessing members inside a namespace requires the scope resolution operator.

**Scope Resolution Operator — `::` -**
1. `::` allows access to members inside a namespace or class.
2. `std::cout` means accessing `cout` inside the `std` namespace.
3. It ensures explicit reference and avoids ambiguity.

**Console Output Object — `std::cout` -**
1. `cout` stands for console output.
2. It is an output stream object.
3. It sends data to the terminal.
4. It belongs to the `std` namespace.

**Stream Insertion Operator — `<<` -**
1. `<<` inserts data into the output stream.
2. It is called the insertion operator.
3. It allows chaining because it returns the stream object.
4. Example:
   - `std::cout << "Age: " << 25;`

**String Literals & Escape Sequences -**
1. Strings are enclosed in double quotes `" "`.
2. Escape sequences begin with a backslash `\`.
3. Common escape sequences:
   - `\n` → New line.
   - `\t` → Tab.
   - `\"` → Double quote.
   - `\\` → Backslash.

**Statement Termination — `;` -**
1. Every C++ statement must end with a semicolon.
2. It signals the end of an instruction.
3. C++ does not allow omission of semicolons.

**Execution Flow -**
1. OS loads the executable into memory.
2. OS calls `main()`.
3. Statements execute sequentially.
4. `return` sends exit status to the OS.
5. Program terminates.

**Core Systems Insight -**
1. C++ enforces explicit structure and strict typing.
2. Entry point and exit status are deterministic.
3. The program directly interacts with the operating system.
4. Even the minimal boilerplate demonstrates system-level control.
5. These properties are foundational for building deterministic trading infrastructure.

---
### C++ Foundations — Variables, Types & Memory Model

C++ is a statically typed, compiled language where every variable has a fixed type and occupies a defined amount of memory. Memory management in C++ is explicit and deterministic, forming the foundation of systems programming.

**Variable Concept -**
1. A variable is a named storage location in memory.
2. The variable name is a label that refers to a specific memory address.
3. When declared, memory is reserved based on its type.
4. Example:
   ```cpp
   int x = 10;
   ```
5. This reserves memory and stores the value `10`.

**Memory Fundamentals -**
1. RAM consists of sequential memory addresses.
2. Each address stores 1 byte.
3. 1 byte = 8 bits.
4. 1 bit stores either 0 or 1.
5. All data is stored in binary form.

**Bit Capacity Rule -**
1. If a type uses N bits, it can represent `2^N` possible bit patterns.
2. Example:
   - 1 bit → 2 values.
   - 2 bits → 4 values.
   - 8 bits → `2^8 = 256` values.
   - 32 bits → `2^32` values.
3. The number of possible values depends solely on number of bits.

**Common Primitive Types -**
1. `int`
   - Typically 4 bytes (32 bits).
   - Stores whole numbers.
2. `double`
   - Typically 8 bytes (64 bits).
   - Stores decimal numbers.
3. `char`
   - 1 byte (8 bits).
   - Stores a single character.
4. `bool`
   - Typically 1 byte.
   - Stores true/false.
5. Exact sizes depend on architecture (32-bit vs 64-bit systems).

**Signed vs Unsigned Integers -**
1. Signed integers store both negative and positive values.
2. Unsigned integers store only non-negative values.
3. For a 32-bit signed int:
   - Range: `-2^31` to `2^31 - 1`.
4. For a 32-bit unsigned int:
   - Range: `0` to `2^32 - 1`.
5. Total possible bit patterns remain `2^32`.

**Declaration vs Initialization -**
1. Declaration:
   ```cpp
   int x;
   ```
   - Memory reserved.
   - Value uninitialized (indeterminate).
2. Initialization:
   ```cpp
   int x = 10;
   ```
   - Memory reserved.
   - Value assigned.
3. Modern safer initialization:
   ```cpp
   int x{10};
   int y{};
   ```
4. Local uninitialized variables contain unpredictable values.
5. Always initialize variables to avoid undefined behavior.

**Stack Memory (Automatic Storage) -**
1. Stack memory is used for local variables and function calls.
2. Allocation and deallocation are automatic.
3. When a function ends, its stack frame is removed.
4. Variables go out of scope and are destroyed immediately.
5. Destruction is deterministic and fast.
6. Stack size is limited.

**Heap Memory (Dynamic Allocation) -**
1. Heap is used for dynamic memory allocation.
2. Memory is allocated using `new`.
   ```cpp
   int* p = new int(10);
   ```
3. `new` allocates memory and returns its address.
4. Heap memory must be manually freed using `delete`.
   ```cpp
   delete p;
   ```
5. If not freed → memory leak.
6. Heap memory lifetime is not tied to scope.

**Pointers -**
1. A pointer is a variable that stores a memory address.
2. Example:
   ```cpp
   int x = 10;
   int* p = &x;
   ```
3. `p` stores address of `x`.
4. `*p` dereferences pointer to access value.
5. Modifying `*p` modifies original variable.
6. Pointers do not copy values; they reference memory.

**Pointer Safety Categories -**
1. Uninitialized Pointer:
   ```cpp
   int* p;
   ```
   - Contains garbage address.
   - Dereferencing causes undefined behavior.
2. Dangling Pointer:
   ```cpp
   int* p = new int(10);
   delete p;
   ```
   - Pointer still holds address of freed memory.
   - Dereferencing causes undefined behavior.
3. Null Pointer:
   ```cpp
   int* p = nullptr;
   ```
   - Explicitly points to nothing.
   - Dereferencing causes immediate crash.
4. Safe practice:
   ```cpp
   delete p;
   p = nullptr;
   ```

**Core Systems Insight -**
1. Type determines memory size.
2. Memory size determines numeric range.
3. Stack memory is automatic and deterministic.
4. Heap memory is manual and flexible.
5. Improper memory management causes leaks and instability.
6. Understanding stack, heap, and pointers is foundational for high-performance systems programming.

---
### C++ Foundations — References & Value Semantics

References in C++ provide an alias to an existing variable. They allow direct access to the same memory location without creating copies, enabling efficient and safer code compared to raw pointers in many cases.

**Reference Concept -**
1. A reference is an alias (another name) for an existing variable.
2. It does not create a new memory location.
3. Example:
   ```cpp
   int x = 10;
   int& ref = x;
   ```
4. Both `x` and `ref` refer to the same memory location.
5. Any modification through `ref` affects `x`.

**Reference Behavior -**
1. Assigning through reference modifies original variable:
   ```cpp
   ref = 20;
   ```
   - Updates `x` to 20.
2. Reference does not create a copy.
3. Reference behaves exactly like the original variable.

**Initialization Rules -**
1. References must be initialized at declaration.
   ```cpp
   int& ref = x;   // valid
   ```
2. Uninitialized references are not allowed:
   ```cpp
   int& ref;   // invalid
   ```
3. A reference cannot be reseated after initialization.

**Reference vs Copy -**
1. Copy creates independent variable:
   ```cpp
   int y = x;
   ```
2. Reference creates alias:
   ```cpp
   int& ref = x;
   ```
3. Modifying copy does not affect original.
4. Modifying reference affects original.

**Reference Chaining -**
1. Multiple references refer to the same original variable:
   ```cpp
   int x = 5;
   int& ref = x;
   int& y = ref;
   ```
2. All refer to `x`.
3. Changes through any reference affect the same value.

**Reference in Functions (Pass by Reference) -**
1. References allow functions to modify original variables:
   ```cpp
   void foo(int& x) {
       x = 50;
   }
   ```
2. No copy is created during function call.
3. Improves performance for large data.
4. Used widely in systems programming.

**Reference vs Pointer -**
1. Pointer stores memory address.
2. Reference is an alias to existing variable.
3. Pointer can be null; reference cannot.
4. Pointer can change target; reference cannot.
5. Pointer requires dereferencing (`*`); reference does not.

**Core Systems Insight -**
1. References eliminate unnecessary copies.
2. Provide safer alternative to pointers in many cases.
3. Enable efficient function parameter passing.
4. Maintain direct access to original memory.
5. Essential for writing high-performance and clean C++ code.

---
### C++ Foundations — Functions & Parameter Passing

Functions in C++ define reusable blocks of code and control execution flow. They create isolated stack frames and determine how data is passed and modified during execution.

**Function Concept -**
1. A function is a reusable block of code that performs a specific task.
2. Every C++ program starts execution from `main()`.
3. Functions can take inputs (parameters) and return outputs.
4. Example:
   ```cpp
   int add(int a, int b) {
       return a + b;
   }
   ```

**Function Execution & Stack Frames -**
1. Each function call creates a new stack frame.
2. The stack frame stores:
   - Parameters.
   - Local variables.
3. When the function finishes:
   - Its stack frame is destroyed.
   - Control returns to the caller.
4. Execution flow:
   - Caller function pauses.
   - Called function executes.
   - Returns value.
   - Caller resumes execution.

**Pass by Value -**
1. Default method of parameter passing.
2. A copy of the variable is created.
3. Changes inside function do not affect original variable.
4. Example:
   ```cpp
   void foo(int x) {
       x = 100;
   }
   ```
5. Original variable remains unchanged.

**Pass by Reference -**
1. Uses reference (`&`) to pass alias of original variable.
2. No copy is created.
3. Changes inside function modify original variable.
4. Example:
   ```cpp
   void foo(int& x) {
       x = 100;
   }
   ```
5. Used for performance and direct modification.

**Pass by Pointer -**
1. Passes memory address of variable.
2. Function accesses value using dereferencing.
3. Example:
   ```cpp
   void foo(int* x) {
       *x = 100;
   }
   ```
4. Called using:
   ```cpp
   foo(&a);
   ```
5. Useful when nullability or dynamic memory is involved.

**Parameter Passing Comparison -**
1. Pass by value:
   - Creates copy.
   - Safe (no side effects).
2. Pass by reference:
   - No copy.
   - Modifies original.
   - Cleaner than pointer.
3. Pass by pointer:
   - Uses address.
   - Requires dereferencing.
   - More flexible but less safe.

**Return Values -**
1. Functions return values using `return`.
2. Returned value is assigned to receiving variable.
3. Example:
   ```cpp
   int square(int x) {
       return x * x;
   }
   ```
4. Used as:
   ```cpp
   int result = square(5);
   ```

**Function Scope -**
1. Variables inside a function exist only within that function.
2. They are destroyed when the function ends.
3. Each function has its own independent scope.

**Core Systems Insight -**
1. Functions control execution flow and memory lifecycle.
2. Stack frames ensure isolation between function calls.
3. Parameter passing determines:
   - Performance.
   - Data safety.
   - Side effects.
4. Choosing between value, reference, and pointer impacts system efficiency.
5. Understanding function behavior is critical for building deterministic systems.

---
### C++ Foundations — Arrays & Memory Layout

Arrays in C++ are collections of elements of the same type stored in contiguous memory. This contiguous layout enables fast and predictable access, making arrays fundamental for performance-critical systems.

**Array Concept -**
1. An array stores multiple elements of the same type.
2. Elements are stored in contiguous memory locations.
3. Example:
   ```cpp
   int arr[3] = {10, 20, 30};
   ```
4. All elements are placed sequentially in memory.

**Contiguous Memory Layout -**
1. Array elements are stored next to each other in memory.
2. Example (conceptual):
   ```
   Address     Value
   0x1000      10
   0x1004      20
   0x1008      30
   ```
3. Each element offset is determined by element size.
4. Enables direct and fast memory access.

**Indexing & Access -**
1. Array elements are accessed using index:
   ```cpp
   arr[0], arr[1], arr[2]
   ```
2. Access is O(1) (constant time).
3. Internally:
   ```
   arr[i] = base_address + (i * size_of_element)
   ```

**Arrays vs JavaScript Arrays -**
1. C++ arrays:
   - Fixed size.
   - Same data type.
   - Contiguous memory.
   - High performance.
2. JavaScript arrays:
   - Dynamic size.
   - Mixed types allowed.
   - Not guaranteed contiguous.
   - More flexible but slower.

**Array Iteration -**
1. Arrays are typically iterated using loops:
   ```cpp
   for (int i = 0; i < 3; i++) {
       std::cout << arr[i];
   }
   ```

**Arrays and Pointers -**
1. Array name represents address of first element.
   ```cpp
   arr == &arr[0]
   ```
2. Pointer arithmetic can be used:
   ```cpp
   *(arr + 1) → second element
   ```
3. Arrays and pointers are closely related in C++.

**Limitations of Arrays -**
1. Size must be known at compile time (for stack arrays).
2. Cannot resize.
3. No bounds checking.
4. Out-of-bounds access leads to undefined behavior.

**Dynamic Arrays (Heap Allocation) -**
1. Arrays can be allocated on heap:
   ```cpp
   int* arr = new int[3];
   ```
2. Elements accessed normally:
   ```cpp
   arr[0], arr[1], arr[2]
   ```
3. Memory must be freed manually:
   ```cpp
   delete[] arr;
   ```
4. Using `delete` instead of `delete[]` is incorrect.

**Stack vs Heap Arrays -**
1. Stack arrays:
   - Automatic allocation and cleanup.
   - Faster.
   - Fixed size.
2. Heap arrays:
   - Manual allocation and cleanup.
   - Flexible size.
   - Slightly slower.

**Cache Friendliness -**
1. Contiguous memory improves CPU cache usage.
2. CPU can prefetch adjacent elements.
3. Leads to faster execution compared to scattered memory structures.

**Core Systems Insight -**
1. Arrays provide predictable and fast memory access.
2. Contiguous layout is critical for performance optimization.
3. Pointer arithmetic enables low-level memory control.
4. Improper bounds handling leads to undefined behavior.
5. Arrays form the foundation for high-performance data structures in systems programming.
6. 
---
### C++ Foundations — Structs & Data Modeling

Structs in C++ allow grouping multiple related variables into a single data type. They are fundamental for modeling real-world entities and organizing data efficiently in systems programming.

**Struct Concept -**
1. A struct groups multiple variables into a single unit.
2. It defines a custom data type.
3. Example:
   ```cpp
   struct Order {
       double price;
       int quantity;
   };
   ```
4. Variables inside struct are called members.
5. Struct improves code organization and readability.

**Struct Usage -**
1. Create struct variable:
   ```cpp
   Order o;
   ```
2. Access members using dot operator:
   ```cpp
   o.price = 101.5;
   o.quantity = 10;
   ```
3. Each struct instance holds its own data.

**Memory Layout -**
1. Struct members are stored in contiguous memory.
2. Order of members is preserved in memory.
3. Example (conceptual):
   ```
   Address     Value
   0x1000      price
   0x1008      quantity
   ```
4. Struct behaves similar to array in memory layout.

**Padding & Alignment -**
1. Struct size may be larger than sum of member sizes.
2. Compiler may add padding for alignment.
3. Improves CPU access efficiency.
4. Example:
   - double (8 bytes) + int (4 bytes) may result in 16 bytes struct.

**Array of Structs -**
1. Multiple structs can be stored in arrays:
   ```cpp
   Order orders[2];
   ```
2. Each struct stored contiguously.
3. Useful for collections of structured data.

**Struct with Pointers -**
1. Struct can be allocated on heap:
   ```cpp
   Order* o = new Order;
   ```
2. Access members using arrow operator:
   ```cpp
   o->price = 101.5;
   ```
3. `->` is used for pointer to struct.

**Dot vs Arrow Operator -**
1. `.` used with object:
   ```cpp
   o.price
   ```
2. `->` used with pointer:
   ```cpp
   o->price
   ```

**Struct Copy Behavior -**
1. Assigning struct copies entire data:
   ```cpp
   Order o2 = o1;
   ```
2. Copy is independent of original.
3. Modifying copy does not affect original.

**Passing Struct to Function -**
1. Pass by value:
   ```cpp
   void foo(Order o);
   ```
   - Creates copy.
   - Expensive for large structs.
2. Pass by reference:
   ```cpp
   void foo(Order& o);
   ```
   - No copy.
   - Modifies original.
3. Preferred approach for performance.

**Struct vs Class (Basic Difference) -**
1. struct → members are public by default.
2. class → members are private by default.
3. Functionality is otherwise similar.

**Core Systems Insight -**
1. Structs model real-world entities (orders, trades, positions).
2. Memory layout directly impacts performance.
3. Copying large structs can be expensive.
4. Passing by reference avoids unnecessary overhead.
5. Structs form the foundation of data modeling in high-performance systems.


---
### C++ Foundations — Classes (Practical OOP)

Classes in C++ provide a way to group data and behavior together while controlling access to internal members. They enable safer and more structured system design compared to raw data structures.

**Class Concept -**
1. A class is similar to a struct but with access control.
2. It allows grouping of data (variables) and behavior (functions).
3. Example:
   ```cpp
   class Order {
   public:
       double price;
       int quantity;
   };
   ```
4. Objects of class can be created like struct instances.

**struct vs class -**
1. struct → members are public by default.
2. class → members are private by default.
3. Functionality is otherwise similar.
4. class provides better control over data access.

**Access Specifiers -**
1. public:
   - Accessible from anywhere.
2. private:
   - Accessible only within the class.
3. protected:
   - Accessible within class and derived classes (advanced use).
4. Default for class is private.

**Encapsulation -**
1. Private members prevent direct external modification.
2. Public functions provide controlled access.
3. Example:
   ```cpp
   class Order {
   private:
       double price;

   public:
       void setPrice(double p) {
           price = p;
       }

       double getPrice() {
           return price;
       }
   };
   ```

**Member Functions -**
1. Functions defined inside class operate on its data.
2. Example:
   ```cpp
   void print() {
       std::cout << price << " " << quantity;
   }
   ```
3. Called using object:
   ```cpp
   o.print();
   ```

**Constructors -**
1. Constructor initializes object during creation.
2. Must have same name as class.
3. No return type.
4. Example:
   ```cpp
   Order(double p, int q) {
       price = p;
       quantity = q;
   }
   ```
5. Automatically called when object is created.

**Initializer List (Preferred) -**
1. More efficient way to initialize members:
   ```cpp
   Order(double p, int q) : price(p), quantity(q) {}
   ```
2. Avoids unnecessary assignments.
3. Preferred in performance-critical systems.

**Object Creation -**
1. Stack allocation:
   ```cpp
   Order o(100, 10);
   ```
2. Heap allocation:
   ```cpp
   Order* o = new Order(100, 10);
   ```

**Dot vs Arrow Operator -**
1. Object access:
   ```cpp
   o.price
   ```
2. Pointer access:
   ```cpp
   o->price
   ```

**Why Classes Matter -**
1. Provide controlled access to data.
2. Prevent accidental modification.
3. Ensure proper initialization through constructors.
4. Combine data and behavior for better design.

**Core Systems Insight -**
1. Classes enforce safe data handling.
2. Encapsulation reduces bugs in complex systems.
3. Constructors ensure objects are always initialized.
4. Proper use of classes improves maintainability.
5. Classes are essential for building structured and scalable systems.

### C++ Foundations — RAII & Resource Management

RAII (Resource Acquisition Is Initialization) is a core C++ principle where resource lifetime is tied to object lifetime. It ensures automatic and deterministic cleanup, eliminating many memory-related bugs.

**Problem with Manual Memory Management -**
1. Memory allocated using `new` must be manually freed using `delete`.
2. Forgetting `delete` leads to memory leaks.
3. Accessing memory after deletion leads to undefined behavior.
4. Exceptions can skip cleanup, causing resource leaks.
5. Manual management is error-prone and unsafe.

**RAII Concept -**
1. Resource acquisition is tied to object initialization.
2. Resource release is tied to object destruction.
3. Object lifetime determines resource lifetime.
4. Cleanup happens automatically when object goes out of scope.

**Constructor & Destructor -**
1. Constructor runs when object is created.
2. Destructor runs when object goes out of scope.
3. Example:
   ```cpp
   class Test {
   public:
       Test() { std::cout << "Created\n"; }
       ~Test() { std::cout << "Destroyed\n"; }
   };
   ```
4. Destructor guarantees cleanup execution.

**RAII for Memory Management -**
1. Resource (memory) is acquired in constructor.
2. Resource is released in destructor.
3. Example:
   ```cpp
   class Wrapper {
       int* ptr;
   public:
       Wrapper(int val) {
           ptr = new int(val);
       }
       ~Wrapper() {
           delete ptr;
       }
   };
   ```
4. No manual delete required by user.

**Smart Pointers (Modern RAII) -**
1. Replace raw pointers with smart pointers.
2. Example:
   ```cpp
   #include <memory>
   std::unique_ptr<int> p = std::make_unique<int>(10);
   ```
3. Automatically deletes memory when out of scope.
4. Prevents memory leaks and dangling pointers.

**std::unique_ptr -**
1. Provides exclusive ownership of resource.
2. Cannot be copied.
3. Ownership can be transferred using `std::move`.
4. Example:
   ```cpp
   auto p = std::make_unique<int>(10);
   ```
5. Ensures only one owner of resource.

**auto Keyword -**
1. Enables type inference.
2. Compiler deduces variable type automatically.
3. Works with all types (primitive, struct, class, pointers).
4. Commonly used with complex types:
   ```cpp
   auto t = std::make_unique<Test>();
   ```
5. Improves readability and reduces verbosity.

**RAII Benefits -**
1. Automatic resource cleanup.
2. Eliminates memory leaks.
3. Prevents use-after-free errors.
4. Ensures exception safety.
5. Provides deterministic behavior.

**Core Systems Insight -**
1. Resource management must be deterministic in high-performance systems.
2. RAII ensures cleanup happens at scope boundaries.
3. Smart pointers replace manual memory handling.
4. Avoid raw `new` and `delete` in modern C++.
5. RAII is fundamental for building stable and safe systems.

---
### C++ Foundations — STL Basics (Practical Toolkit)

The Standard Template Library (STL) provides ready-to-use data structures and utilities in C++. It enables efficient and safe handling of data without manual memory management.

**STL Concept -**
1. STL stands for Standard Template Library.
2. Provides commonly used data structures and algorithms.
3. Eliminates need to build basic data structures from scratch.
4. Works seamlessly with RAII for automatic memory management.

**std::vector (Dynamic Array) -**
1. A vector is a dynamic array with automatic resizing.
2. Stores elements in contiguous memory.
3. Example:
   ```cpp
   #include <vector>
   std::vector<int> v = {1, 2, 3};
   ```
4. Supports fast random access (O(1)).

**Vector Operations -**
1. Add element:
   ```cpp
   v.push_back(4);
   ```
2. Access elements:
   ```cpp
   v[0]        // fast access
   v.at(0)     // safe access with bounds checking
   ```
3. Get size:
   ```cpp
   v.size();
   ```
4. Iterate:
   ```cpp
   for (int x : v) {
       std::cout << x;
   }
   ```

**Vector Memory Behavior -**
1. Uses contiguous memory (like arrays).
2. Automatically resizes when capacity is exceeded.
3. Reallocation involves:
   - Allocating new memory.
   - Copying old elements.
   - Releasing old memory.
4. Reallocation can be expensive.

**Vector Optimization -**
1. Reserve memory in advance:
   ```cpp
   v.reserve(100);
   ```
2. Avoids repeated reallocations.
3. Improves performance in high-frequency operations.

**std::unordered_map (Hash Map) -**
1. Stores key-value pairs.
2. Provides average O(1) lookup time.
3. Example:
   ```cpp
   #include <unordered_map>
   std::unordered_map<int, int> m;
   ```
4. Insert:
   ```cpp
   m[1] = 100;
   ```
5. Access:
   ```cpp
   m[1];
   ```
6. Check existence:
   ```cpp
   if (m.find(1) != m.end()) {
   }
   ```

**Vector vs unordered_map -**
1. vector:
   - Sequential data.
   - Fast iteration.
   - Index-based access.
2. unordered_map:
   - Key-value lookup.
   - Fast search.
   - No ordering guarantee.

**Copy vs Reference Behavior -**
1. Copy:
   ```cpp
   auto v2 = v;
   ```
   - Creates independent copy.
   - Modifications do not affect original.
2. Reference:
   ```cpp
   auto& v2 = v;
   ```
   - No copy.
   - Both refer to same data.
   - Modifications affect original.

**STL and RAII -**
1. STL containers manage memory automatically.
2. No need for manual `new` or `delete`.
3. Memory is released when container goes out of scope.
4. Provides safety and reliability.

**Core Systems Insight -**
1. STL provides efficient and optimized data structures.
2. Contiguous memory in vector enables high performance.
3. Understanding copy vs reference is critical for performance.
4. Pre-allocation improves efficiency in real-time systems.
5. STL combined with RAII enables safe and maintainable system design.

---
### C++ Foundations — Compilation & Build Basics

C++ is a compiled language where source code is transformed into machine code before execution. Understanding the compilation process is essential for building and running performant systems.

**Compilation Concept -**
1. C++ code is not executed directly.
2. Source code must be compiled into an executable.
3. Flow:
   ```
   Source Code (.cpp) → Compiler → Executable → Run
   ```
4. Compilation ensures correctness before execution.

**Compilation Steps -**
1. Compilation:
   - Checks syntax and type correctness.
   - Converts code into intermediate machine instructions.
2. Linking:
   - Connects external libraries and dependencies.
   - Resolves function and symbol references.
3. Output:
   - Generates executable binary.

**Basic Compilation Command -**
1. Using g++:
   ```bash
   g++ main.cpp -o app
   ```
2. Output executable named `app`.
3. Run using:
   ```bash
   ./app
   ```

**Compile-Time vs Runtime Errors -**
1. Compile-time errors:
   - Detected during compilation.
   - Example:
     ```cpp
     int x = "hello";
     ```
2. Runtime errors:
   - Occur during execution.
   - Example:
     ```cpp
     int* p = nullptr;
     std::cout << *p;
     ```

**Optimization Flags -**
1. Compiler optimizations improve performance.
2. Example:
   ```bash
   g++ main.cpp -o app -O2
   ```
3. Higher optimization can improve speed but may increase compile time.

**Multi-file Compilation (Basic Idea) -**
1. Large programs are split across multiple files.
2. Example:
   ```
   main.cpp
   order.cpp
   order.h
   ```
3. Compiled together:
   ```bash
   g++ main.cpp order.cpp -o app
   ```

**C++ vs Interpreted Languages -**
1. C++:
   - Compiled.
   - Faster execution.
   - Errors caught early.
2. JavaScript:
   - Interpreted/JIT.
   - More flexible.
   - Errors often occur at runtime.

**Core Systems Insight -**
1. Compilation enables direct machine-level execution.
2. Eliminates runtime interpretation overhead.
3. Improves performance and predictability.
4. Early error detection increases system reliability.
5. Efficient build process is essential for scalable system development.