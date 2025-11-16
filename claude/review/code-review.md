Perform comprehensive code review for recent changes: $ARGUMENTS

## Code Review Process

### 1. Change Analysis
- Identify all modified files and understand scope of changes
- Review commit messages for clarity and conventional commit compliance
- Check if changes align with stated requirements/tickets
- Assess impact on existing functionality

### 2. Code Quality Assessment

#### **Structure & Architecture**
- [ ] Follows established project patterns and conventions
- [ ] Proper separation of concerns (no god classes/functions)
- [ ] Appropriate use of design patterns
- [ ] Code is in the right layer/module for its functionality

#### **ROS2 Specific Standards**
- [ ] Proper lifecycle management for nodes
- [ ] Correct use of ROS2 idioms (composition, parameters, QoS)
- [ ] Topic/service/action naming follows conventions (snake_case)
- [ ] Thread safety considerations for callback handling
- [ ] Proper error handling and logging practices

#### **Code Style & Readability**  
- [ ] Consistent formatting (clang-format for C++, black for Python)
- [ ] Meaningful variable and function names
- [ ] Appropriate comments for complex logic
- [ ] No commented-out code blocks
- [ ] Documentation strings for public APIs

### 3. Functionality Review

#### **Logic & Correctness**
- [ ] Algorithm implementation matches specifications
- [ ] Edge cases are properly handled
- [ ] Error conditions are caught and handled gracefully
- [ ] Resource management (memory, file handles, network connections)
- [ ] Race conditions and concurrency issues addressed

#### **Performance Considerations**
- [ ] No obvious performance bottlenecks
- [ ] Appropriate data structures for use cases
- [ ] Efficient algorithms chosen for problem scale
- [ ] Memory allocation patterns are reasonable
- [ ] Hot paths are optimized

### 4. Testing & Validation

#### **Test Coverage**
- [ ] Unit tests exist for new functionality
- [ ] Integration tests cover interaction points
- [ ] Test cases include edge cases and error conditions
- [ ] Mock objects used appropriately for external dependencies
- [ ] Test names clearly describe what's being tested

#### **Test Quality**
- [ ] Tests are deterministic and repeatable
- [ ] No test dependencies on external state
- [ ] Proper setup and teardown procedures
- [ ] Tests run quickly enough for CI/CD pipeline

### 5. Security & Safety Review

#### **ROS2 Security**
- [ ] No hardcoded credentials or sensitive data
- [ ] Proper input validation for external data
- [ ] Safe handling of network communications
- [ ] Appropriate access controls and permissions

#### **Robot Safety**
- [ ] Emergency stop capabilities preserved
- [ ] Safety limits and bounds checking
- [ ] Graceful degradation on sensor failures
- [ ] No unsafe default behaviors

### 6. Documentation & Maintenance

#### **Documentation Updates**
- [ ] README updated for new features/changes
- [ ] API documentation reflects changes
- [ ] Configuration parameters documented
- [ ] Launch file examples provided

#### **Maintainability**
- [ ] Code is easy to understand and modify
- [ ] Dependencies are minimal and justified
- [ ] Configuration is externalized appropriately
- [ ] Logging provides useful debugging information

### 7. Review Output Format

#### **Summary**
- Overall assessment (Approve/Request Changes/Comment)
- Key strengths of the implementation
- Critical issues that must be addressed
- Suggested improvements for future consideration

#### **Detailed Feedback**
- Line-by-line comments for specific issues
- Suggestions for alternative approaches
- Performance optimization opportunities
- Testing gaps and recommended additions

#### **Action Items**
- Must-fix issues before merge
- Nice-to-have improvements
- Follow-up tasks for future iterations
- Documentation updates needed

### 8. Review Guidelines
- Focus on correctness, maintainability, and safety
- Provide constructive feedback with specific suggestions
- Consider the change's impact on the broader system
- Balance thoroughness with development velocity
- Ask questions when requirements or design decisions are unclear

Be thorough but practical. The goal is shipping robust, maintainable code while fostering team learning and code quality.