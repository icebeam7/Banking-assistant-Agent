import pytest
from agent_framework import MCPStreamableHTTPTool
from mcp.types import Tool


def test_mcp_tool_supports_agent_framework_schema_api():
    tool = Tool(name="test_tool", inputSchema={})

    assert tool.inputSchema == {}


@pytest.mark.asyncio
async def test_agent_framework_discovers_streamable_http_tools(mock_mcp_servers):
    account_port = mock_mcp_servers["account"]
    tool = MCPStreamableHTTPTool(
        name="Account MCP compatibility test",
        url=f"http://127.0.0.1:{account_port}/mcp/mcp",
    )

    try:
        await tool.connect()

        assert "getAccountsByUserName" in {function.name for function in tool.functions}
    finally:
        await tool.close()
