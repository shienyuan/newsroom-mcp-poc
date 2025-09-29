"""Greeting prompt template implementation.

This module provides a reusable prompt template for generating personalized
greetings with different styles.
"""


def register_prompts(mcp):
    """Register all prompts from this module with the MCP server.
    
    Args:
        mcp: FastMCP server instance to register prompts with.
    """
    @mcp.prompt(
        name="greeting_template",
        description="A simple prompt template for generating personalized greetings",
        tags={"greeting", "template"}
    )
    def greeting_template(name: str, style: str = "casual") -> str:
        """Generate a personalized greeting prompt.
        
        This prompt template creates instructions for generating greetings
        with different styles (formal or casual). It demonstrates how to
        create reusable prompt templates with parameters.
        
        Args:
            name: The name of the person to greet (required).
            style: The greeting style - "formal" or "casual" (optional, defaults to "casual").
            
        Returns:
            str: A prompt template string for generating the greeting.
            
        Example:
            Input: {"name": "Alice", "style": "formal"}
            Output: "Generate a formal greeting for Alice.
                     The greeting should be professional and respectful."
                     
            Input: {"name": "Bob", "style": "casual"}
            Output: "Generate a casual greeting for Bob.
                     The greeting should be friendly and warm."
        """
        if style.lower() == "formal":
            return f"""Generate a formal greeting for {name}.
The greeting should be professional and respectful."""
        else:
            return f"""Generate a casual greeting for {name}.
The greeting should be friendly and warm."""

