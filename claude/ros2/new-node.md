Create a new ROS2 node: $ARGUMENTS

## Node Creation Process
1. **Analyze Requirements**:
   - Parse the node description and requirements
   - Identify required topics (publishers/subscribers)
   - Determine services or actions needed
   - Consider parameter requirements

2. **Package Structure**:
   - Create or use existing ROS2 package
   - Set up proper CMakeLists.txt and package.xml
   - Create appropriate directory structure (src/, include/, launch/, etc.)

3. **Node Implementation**:
   - Create C++ or Python node based on project preference
   - Implement proper ROS2 lifecycle if needed
   - Add parameter handling with validation
   - Include proper error handling and logging
   - Follow ROS2 best practices for naming and structure

4. **Supporting Files**:
   - Create launch file with proper parameter configuration
   - Add configuration YAML files if needed
   - Create any custom message/service/action files
   - Set up proper dependencies in package.xml

5. **Testing & Documentation**:
   - Create basic unit tests
   - Add integration test if interacting with other nodes
   - Create README with usage instructions
   - Document parameters and their expected values

## Standards to Follow
- Use project's existing coding style and conventions
- Follow ROS2 naming conventions (snake_case for topics/services)
- Include proper error handling and graceful shutdown
- Add meaningful log messages for debugging
- Use appropriate QoS settings for topics

## Ask Before Implementation
- Programming language preference (C++ or Python)?
- Should this be a lifecycle node?
- Any specific QoS requirements for topics?
- Integration requirements with existing nodes?

Ready to create a production-ready ROS2 node!