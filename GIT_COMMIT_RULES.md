# Git Commit Rules for claw-cog

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

## Examples

```
feat(self_awareness): add identity loading from file

- Support loading identity from IDENTITY.md
- Parse identity fields from markdown format
- Add error handling for missing files

Closes #123
```

```
fix(reflective): correct lesson extraction logic

The lesson extraction was not properly handling failed actions.
This fix ensures lessons are extracted from both successful and
failed actions.

Fixes #456
```

## Best Practices

1. Keep commits atomic (one logical change per commit)
2. Write clear, descriptive subjects
3. Reference issues in footer
4. Ensure tests pass before committing
5. Use English for all commit messages (project requirement)
