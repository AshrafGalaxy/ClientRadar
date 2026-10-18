# Git Guidelines

## Git Commit Rules
- Always use specialized, simple, clear, and understandable git commit messages.
- Use standard conventional commit format: `<type>: <summary>`.
- The commit title/subject MUST be strictly under 60 characters.
- When necessary, provide proper commit message details in the body (explaining what changed and why).

### Standard Format
```text
<type>: <short imperative summary under 60 chars>

[optional body with details]
- Bullet point detail 1
- Bullet point detail 2
```

### Allowed Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to build process or auxiliary tools and libraries

`git`
