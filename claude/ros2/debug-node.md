Debug ROS2 node issues: $ARGUMENTS

## Debugging Process
1. **Issue Analysis**:
   - Understand the problem description
   - Identify which node(s) are affected
   - Determine if it's runtime, build, or communication issue

2. **Systematic Investigation**:
   - Check ROS2 node status: `ros2 node list`
   - Verify topic connections: `ros2 topic list` and `ros2 topic info`
   - Examine logs: `ros2 launch --log-level debug`
   - Check parameter values: `ros2 param list` and `ros2 param get`

3. **Common Issue Categories**:
   - **Communication Issues**: Topic/service connectivity, QoS mismatches
   - **Performance Issues**: High CPU/memory usage, slow message processing  
   - **Logic Issues**: Incorrect behavior, state management problems
   - **Integration Issues**: Node interactions, timing problems

4. **Diagnostic Tools**:
   - Use `rqt_graph` to visualize node connections
   - Monitor with `rqt_topic` or `rqt_plot` for data inspection
   - Check system resources with `htop` or similar
   - Use `ros2 bag` to record/replay scenarios

5. **Solution Implementation**:
   - Provide specific fixes with code changes
   - Suggest configuration adjustments
   - Recommend architectural improvements if needed
   - Include verification steps to confirm the fix

## Questions to Clarify
- What specific symptoms are you observing?
- When did the issue start occurring?
- Are there any error messages in the logs?
- Which nodes or topics are involved?
- Can you reproduce the issue consistently?

Let's systematically identify and fix the ROS2 issue!