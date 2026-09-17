# Rule identities

Every rule file has a stable `identity`.  A rule is identified across this
profile by the pair `identity:id`, where `id` is the positive integer local to
its rule file.  The identity is deliberately independent of a file's taxonomy
`section` so that taxonomy can evolve without changing references to rules.
