# Error Message Improvement Guide

**Last Updated:** 2025-11-09
**Status:** ✅ COMPLETE - All 12 skills (48 operations, ~200 error handlers) have agent-friendly error messages

---

## 🎯 Overview

This guide documents the pattern for improving error messages across all skill operations to make them agent-friendly. Agent-friendly errors include:

1. **Clear, actionable error messages**
2. **Specific suggestions** for fixing the error
3. **Example fixes** showing correct usage

---

## ✅ Completed Skills (12/12) - 100% COMPLETE!

### Week 1 (Top 3 Skills)
1. ✅ **test_orchestrator** (3 operations) - Complete
2. ✅ **code_analysis** (3 operations) - Complete
3. ✅ **learning_plan_manager** (3 operations) - Complete

### Week 8 (Refactor Assistant)
4. ✅ **refactor_assistant** (4 operations) - Complete

### Week 9 (All Remaining Skills)
5. ✅ **context_manager** (3 operations) - Complete
6. ✅ **dependency_guardian** (3 operations) - Complete
7. ✅ **pr_review_assistant** (4 operations) - Complete
8. ✅ **git_workflow_assistant** (4 operations) - Complete
9. ✅ **doc_generator** (3 operations) - Complete
10. ✅ **code_search** (4 operations) - Complete
11. ✅ **skill_evaluator** (10 operations) - Complete
12. ✅ **spec_to_implementation** (2 operations) - Complete

**All operations complete!** 🎉

---

## 📋 Error Message Pattern

### Before (Basic Error)

```python
except FileNotFoundError:
    return OperationResult(
        success=False,
        error=f"File not found: {file_path}",
        error_code="FILE_NOT_FOUND",
        duration=time.time() - start_time
    )
```

**Problems:**
- ❌ No guidance on how to fix
- ❌ Agent doesn't know what to try next
- ❌ No example of correct usage

### After (Agent-Friendly Error)

```python
except FileNotFoundError:
    return OperationResult(
        success=False,
        error=f"Cannot find file: {file_path}",
        error_code="FILE_NOT_FOUND",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Check if the file path is correct",
                "Use Glob('**/*.py') to find Python files",
                f"Verify the file exists with Bash('ls -la {Path(file_path).parent}')"
            ],
            "example_fix": "operation_name('src/correct/path.py')"
        }
    )
```

**Benefits:**
- ✅ Clear, actionable suggestions
- ✅ Agent knows what tools to use
- ✅ Example shows correct usage

---

## 🔧 Common Error Types and Patterns

### 1. FileNotFoundError

**Context:** File path provided doesn't exist

**Pattern:**
```python
except FileNotFoundError:
    return OperationResult(
        success=False,
        error=f"Cannot find file: {file_path}",
        error_code="FILE_NOT_FOUND",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Check if the file path is correct",
                "Use Glob('**/*.py') to find files in the project",
                f"Verify the file exists with Bash('ls -la {Path(file_path).parent}')"
            ],
            "example_fix": f"{operation_name}('src/actual/file.py')"
        }
    )
```

### 2. SyntaxError

**Context:** Python file has syntax errors

**Pattern:**
```python
except SyntaxError as e:
    return OperationResult(
        success=False,
        error=f"Python syntax error in {file_path}: {str(e)}",
        error_code="SYNTAX_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Fix syntax errors in the file before analysis",
                f"Run: Bash('python -m py_compile {file_path}') to see detailed errors",
                "Consider analyzing a different file first"
            ],
            "example_fix": f"# Fix syntax first, then: {operation_name}('src/fixed_file.py')"
        }
    )
```

### 3. ValueError (Invalid Parameters)

**Context:** Operation parameters are invalid

**Pattern:**
```python
except ValueError as e:
    return OperationResult(
        success=False,
        error=f"Invalid parameters: {str(e)}",
        error_code="VALIDATION_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Check parameter types match the expected format",
                "Verify all required parameters are provided",
                "See operation docstring for valid parameter values"
            ],
            "example_fix": f"{operation_name}('file.py', param1='valid_value', param2=10)"
        }
    )
```

### 4. Generic Exception

**Context:** Unexpected error during operation

**Pattern:**
```python
except Exception as e:
    return OperationResult(
        success=False,
        error=f"Operation failed: {str(e)}",
        error_code="OPERATION_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Check if the input data is valid",
                "Try with simpler input first to verify operation works",
                "Check file encoding if working with files (should be UTF-8)"
            ],
            "example_fix": f"{operation_name}('simple_input.py')"
        }
    )
```

---

## 📝 Skill-Specific Patterns

### context_manager

**Operations:** analyze_context, create_notes, compact_conversation

**Common Errors:**
- FileNotFoundError (notes directory)
- ValueError (invalid time period)
- Exception (context analysis failed)

**Example:**
```python
# analyze_context
except ValueError as e:
    return OperationResult(
        success=False,
        error=f"Invalid time period: {str(e)}",
        error_code="VALIDATION_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Time period should be in format '7d', '30d', etc.",
                "Valid units: d (days), h (hours), m (minutes)",
                "Ensure the time period is a positive number"
            ],
            "example_fix": "analyze_context(time_period='30d')"
        }
    )
```

### dependency_guardian

**Operations:** analyze_dependencies, check_vulnerabilities, check_updates

**Common Errors:**
- FileNotFoundError (requirements.txt, package.json)
- ValueError (unsupported ecosystem)
- Exception (network error, API timeout)

**Example:**
```python
# check_vulnerabilities
except FileNotFoundError:
    return OperationResult(
        success=False,
        error=f"Cannot find dependency file in {project_path}",
        error_code="FILE_NOT_FOUND",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Ensure requirements.txt (Python) or package.json (Node) exists",
                "Check if you're in the correct project directory",
                "Use Bash('find . -name requirements.txt') to locate dependency files"
            ],
            "example_fix": "check_vulnerabilities('path/to/project/')"
        }
    )
```

### pr_review_assistant

**Operations:** review_pull_request, analyze_change_impact, check_pr_quality

**Common Errors:**
- ValueError (invalid PR ID)
- Exception (GitHub API error, PR not found)

**Example:**
```python
# review_pull_request
except ValueError as e:
    return OperationResult(
        success=False,
        error=f"Invalid PR ID: {str(e)}",
        error_code="VALIDATION_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "PR ID should be a positive integer",
                "Use Bash('gh pr list') to see available PRs",
                "Verify the PR exists in the repository"
            ],
            "example_fix": "review_pull_request(pr_id=123)"
        }
    )
```

### git_workflow_assistant

**Operations:** analyze_changes, generate_commit_message, suggest_branch_name, create_pull_request

**Common Errors:**
- Exception (not a git repository, no changes)

**Example:**
```python
# analyze_changes
except Exception as e:
    if "not a git repository" in str(e).lower():
        return OperationResult(
            success=False,
            error=f"Not a git repository: {str(e)}",
            error_code="NOT_GIT_REPO",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Ensure you're in a git repository",
                    "Run: Bash('git status') to verify git is initialized",
                    "Initialize git with: Bash('git init') if needed"
                ],
                "example_fix": "# cd to git repo, then: analyze_changes()"
            }
        )
    else:
        return OperationResult(
            success=False,
            error=f"Git operation failed: {str(e)}",
            error_code="GIT_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if you have uncommitted changes: Bash('git status')",
                    "Verify git is properly configured",
                    "Ensure you have permission to access the repository"
                ],
                "example_fix": "analyze_changes()"
            }
        )
```

### doc_generator

**Operations:** generate_docstrings, generate_readme, analyze_documentation

**Common Errors:**
- FileNotFoundError (file/directory not found)
- SyntaxError (invalid Python)
- ValueError (invalid docstring style)

**Example:**
```python
# generate_docstrings
except ValueError as e:
    return OperationResult(
        success=False,
        error=f"Invalid docstring style: {str(e)}",
        error_code="VALIDATION_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Valid styles are: 'google', 'numpy', 'sphinx'",
                "Check the style parameter spelling",
                "Use 'google' style for most cases (default)"
            ],
            "example_fix": "generate_docstrings('file.py', style='google')"
        }
    )
```

### code_search

**Operations:** search_symbol, search_pattern, find_definition, find_usages

**Common Errors:**
- FileNotFoundError (project path not found)
- ValueError (invalid symbol type, invalid pattern)

**Example:**
```python
# search_symbol
except ValueError as e:
    return OperationResult(
        success=False,
        error=f"Invalid symbol type: {str(e)}",
        error_code="VALIDATION_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Valid symbol types: 'function', 'class', 'variable', 'all'",
                "Check the symbol_type parameter",
                "Use 'all' to search for any symbol type"
            ],
            "example_fix": "search_symbol('UserAuth', symbol_type='class')"
        }
    )
```

### skill_evaluator

**Operations:** monitor_execution, evaluate_quality, analyze_performance, etc. (10 total)

**Common Errors:**
- ValueError (no execution data, insufficient data)
- Exception (analysis failed)

**Example:**
```python
# evaluate_quality
# Note: This skill already returns OperationResult with error handling in the try block
# for INSUFFICIENT_DATA cases, so focus on other exceptions

except Exception as e:
    return OperationResult(
        success=False,
        error=f"Quality evaluation failed: {str(e)}",
        error_code="EVALUATION_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Ensure the skill has execution history",
                "Try with a skill that has been used recently",
                "Check if the skill name is correct"
            ],
            "example_fix": "evaluate_quality('test_orchestrator', execution_samples=50)"
        }
    )
```

### spec_to_implementation

**Operations:** implement_from_spec, analyze_spec

**Common Errors:**
- FileNotFoundError (spec file not found)
- ValueError (invalid spec format)
- Exception (implementation failed)

**Example:**
```python
# implement_from_spec
except ValueError as e:
    return OperationResult(
        success=False,
        error=f"Invalid specification: {str(e)}",
        error_code="VALIDATION_ERROR",
        duration=time.time() - start_time,
        metadata={
            "suggestions": [
                "Check if the spec file is in valid markdown format",
                "Ensure the spec has required sections",
                "Try analyze_spec first to validate the specification"
            ],
            "example_fix": "implement_from_spec('specs/feature.md', 'output/')"
        }
    )
```

---

## 🎯 Implementation Checklist

For each remaining skill:

- [ ] Identify all operations in operations.py
- [ ] For each operation:
  - [ ] Find all exception handlers
  - [ ] Add `metadata` dict with `suggestions` and `example_fix`
  - [ ] Improve error message clarity
  - [ ] Add operation-specific suggestions
  - [ ] Provide realistic example fix
- [ ] Test error handling with invalid inputs
- [ ] Update skill documentation if needed

---

## 📊 Progress Tracking

### Operations Updated

| Skill | Operations | Status |
|-------|-----------|--------|
| test_orchestrator | 3 | ✅ Complete |
| code_analysis | 3 | ✅ Complete |
| learning_plan_manager | 3 | ✅ Complete |
| refactor_assistant | 4 | ✅ Complete |
| context_manager | 3 | ✅ Complete |
| dependency_guardian | 3 | ✅ Complete |
| pr_review_assistant | 4 | ✅ Complete |
| git_workflow_assistant | 4 | ✅ Complete |
| doc_generator | 3 | ✅ Complete |
| code_search | 4 | ✅ Complete |
| skill_evaluator | 10 | ✅ Complete |
| spec_to_implementation | 2 | ✅ Complete |

**Completed:** 48 operations (100%)
**Phase 3.2: COMPLETE! 🎉**

---

## 🎓 Best Practices

### DO ✅

1. **Be specific** - Tell agents exactly what's wrong
2. **Provide tools** - Suggest Glob, Grep, Bash commands
3. **Give examples** - Show correct usage
4. **Be actionable** - Each suggestion should be something the agent can do
5. **Context matters** - Tailor suggestions to the operation
6. **Use metadata** - Keep suggestions and examples in metadata for easy access

### DON'T ❌

1. **Don't be vague** - "Something went wrong" is not helpful
2. **Don't just restate** - Suggestions shouldn't just repeat the error
3. **Don't provide invalid examples** - Examples must actually work
4. **Don't forget error_code** - Always include for programmatic handling
5. **Don't skip duration** - Always calculate and return duration

---

## 📝 Example: Complete Operation Error Handling

Here's a complete example showing all error types for a typical operation:

```python
def operation_name(
    file_path: str,
    param: str = "default",
    response_format: str = "summary",
    **kwargs
) -> OperationResult:
    """Operation description."""
    start_time = time.time()

    try:
        # Operation logic
        result = _do_operation(file_path, param)

        # Format response
        duration = time.time() - start_time
        return OperationResult(
            success=True,
            data=result,
            duration=duration
        )

    except FileNotFoundError:
        return OperationResult(
            success=False,
            error=f"Cannot find file: {file_path}",
            error_code="FILE_NOT_FOUND",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if the file path is correct",
                    "Use Glob('**/*.py') to find files",
                    f"Verify the file exists with Bash('ls -la {Path(file_path).parent}')"
                ],
                "example_fix": f"operation_name('src/correct/file.py', param='value')"
            }
        )

    except SyntaxError as e:
        return OperationResult(
            success=False,
            error=f"Python syntax error in {file_path}: {str(e)}",
            error_code="SYNTAX_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Fix syntax errors before running operation",
                    f"Run: Bash('python -m py_compile {file_path}') for details",
                    "Try with a syntactically correct file"
                ],
                "example_fix": "# Fix syntax first, then retry"
            }
        )

    except ValueError as e:
        return OperationResult(
            success=False,
            error=f"Invalid parameter value: {str(e)}",
            error_code="VALIDATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check parameter types and values",
                    "See docstring for valid parameter values",
                    "Verify all required parameters are provided"
                ],
                "example_fix": f"operation_name('file.py', param='valid_value')"
            }
        )

    except Exception as e:
        return OperationResult(
            success=False,
            error=f"Operation failed: {str(e)}",
            error_code="OPERATION_ERROR",
            duration=time.time() - start_time,
            metadata={
                "suggestions": [
                    "Check if input data is valid",
                    "Try with simpler input to verify operation works",
                    "Check file encoding (should be UTF-8)"
                ],
                "example_fix": f"operation_name('simple_file.py')"
            }
        )
```

---

## 🔗 Related Documentation

- `docs/ANTHROPIC_BEST_PRACTICES_IMPLEMENTATION_PLAN.md` - Overall plan
- `docs/TOKEN_EFFICIENCY_GUIDE.md` - Token optimization patterns
- `skills/test_orchestrator/operations.py` - Reference implementation

---

*Last Updated: 2025-11-09*
*Status: ✅ COMPLETE - All 12 skills done!*
*Completion: 100% (48/48 operations)*
