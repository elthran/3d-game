## What are Initializers?

They establish a pipeline for importing external packages, components, models and the game instance. This pipeline will supposedly avoid the recursive import problem by establishing a standard import order.

i.e.

1. exteranl libraries are import first.
2. then the game instance is intitialized.
	i. the game instance imports components (which are models) and models
	ii. Models import nothing except other models (an possibly shouldn't even do that).
3. The internal initializers are called next and they import controllers as necessary (which I don't like). Each initializer first imports the game package then modifies the game instance as necessary to do whatever they are supposed to do (like add lighting).
4. Controllers import the game instance package ... which I don't like.
I really want to figure out how the 'render' global was established and use that pattern.
