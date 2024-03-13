"""Test ChatNVIDIA chat model."""
import pytest
import warnings

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from langchain_nvidia_ai_endpoints.chat_models import ChatNVIDIA


#
# we setup an --all-models flag in conftest.py, when passed it configures chat_model and image_in_model to be all
# available models of type chat or image_in
#
# note: currently --all-models only works with the default mode because different modes may have different available models
#


def test_chat_ai_endpoints(chat_model) -> None:
    """Test ChatNVIDIA wrapper."""
    chat = ChatNVIDIA(
        model=chat_model,
        temperature=0.7,
    )
    message = HumanMessage(content="Hello")
    response = chat.invoke([message])
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)


def test_chat_ai_endpoints_model() -> None:
    """Test wrapper handles model."""
    chat = ChatNVIDIA(model="mistral")
    assert chat.model == "mistral"


def test_chat_ai_endpoints_system_message(chat_model) -> None:
    """Test wrapper with system message."""
    chat = ChatNVIDIA(model=chat_model, max_tokens=36)
    system_message = SystemMessage(content="You are to chat with the user.")
    human_message = HumanMessage(content="Hello")
    response = chat([system_message, human_message])
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)


## TODO: Not sure if we want to support the n syntax. Trash or keep test


def test_ai_endpoints_streaming(chat_model) -> None:
    """Test streaming tokens from ai endpoints."""
    llm = ChatNVIDIA(model=chat_model, max_tokens=36)

    for token in llm.stream("I'm Pickle Rick"):
        assert isinstance(token.content, str)


async def test_ai_endpoints_astream(chat_model) -> None:
    """Test streaming tokens from ai endpoints."""
    llm = ChatNVIDIA(model=chat_model, max_tokens=35)

    async for token in llm.astream("I'm Pickle Rick"):
        assert isinstance(token.content, str)


async def test_ai_endpoints_abatch(chat_model) -> None:
    """Test streaming tokens."""
    llm = ChatNVIDIA(model=chat_model, max_tokens=36)

    result = await llm.abatch(["I'm Pickle Rick", "I'm not Pickle Rick"])
    for token in result:
        assert isinstance(token.content, str)


async def test_ai_endpoints_abatch_tags(chat_model) -> None:
    """Test batch tokens."""
    llm = ChatNVIDIA(model=chat_model, max_tokens=55)

    result = await llm.abatch(
        ["I'm Pickle Rick", "I'm not Pickle Rick"], config={"tags": ["foo"]}
    )
    for token in result:
        assert isinstance(token.content, str)


def test_ai_endpoints_batch(chat_model) -> None:
    """Test batch tokens."""
    llm = ChatNVIDIA(model=chat_model, max_tokens=60)

    result = llm.batch(["I'm Pickle Rick", "I'm not Pickle Rick"])
    for token in result:
        assert isinstance(token.content, str)


async def test_ai_endpoints_ainvoke(chat_model) -> None:
    """Test invoke tokens."""
    llm = ChatNVIDIA(model=chat_model, max_tokens=60)

    result = await llm.ainvoke("I'm Pickle Rick", config={"tags": ["foo"]})
    assert isinstance(result.content, str)


def test_ai_endpoints_invoke(chat_model) -> None:
    """Test invoke tokens."""
    llm = ChatNVIDIA(model=chat_model, max_tokens=60)

    result = llm.invoke("I'm Pickle Rick", config=dict(tags=["foo"]))
    assert isinstance(result.content, str)




def test_image_in_models(image_in_model) -> None:
    try:
        chat = ChatNVIDIA(model=image_in_model)
        response = chat.invoke([
            HumanMessage(
                content=[
                    {"type": "text", "text": "Describe this image:"},
                    {"type": "image_url", "image_url": {"url": "tests/data/nvidia-picasso.jpg"}},
                ]
            )])
        assert isinstance(response, BaseMessage)
        assert isinstance(response.content, str)
    except TimeoutError as e:
        message = f"TimeoutError: {image_in_model} {e}"
        warnings.warn(message)
        pytest.skip(message)
