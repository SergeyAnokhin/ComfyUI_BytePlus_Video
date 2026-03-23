Generate coherent and clear text content based on the input prompts. New user of ModelArk? Please refer to [Quick Start ](/docs/undefined/693ab5c4f3ed61056129105f)for information on obtaining an API key and setting up models, and other necessary preparations.
<span id="18cf565a"></span>
# Quick start with samples

<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.39429928741092635);">

Input

   ```Plain Text
   Please structure the following content: ModelArk is a large model service platform launched by BytePlus, providing comprehensive functions and services such as model training, inference, evaluation, and fine-tuning, and focusing on supporting the large model ecosystem. ModelArk ensures the model security of model providers and the information security of model users through a stable and reliable security mutual trust scheme, accelerating the penetration of large model capabilities into all industries and helping model providers and users achieve new business growth.
   ```



</div>
<div style="flex-shrink: 0;width: calc((100% - 16px) * 0.6057007125890737);margin-left: 16px;">

Output preview

   ```Plain Text
   # Structured Information about ModelArk
   
   ## I. Basic Attributes
   
   1. **Launching Entity**: BytePlus
   2. **Platform Positioning**: Large Model Service Platform
   
   ## II. Core Functions and Services
   Provides comprehensive functions and services related to large models, including model training, inference, evaluation, and fine-tuning. Core positioning includes:
   
   1. Supporting the construction of the large model ecosystem. 
   2. Promoting the penetration of large model capabilities into various industries. 
   
   ## III. Security Assurance Plan
   Uses stable and reliable security and trust solutions to ensure information security in both directions:
   
   1. Model Providers: Ensuring the security of their models.
   2. Model Users: Ensuring the security of their information.
   
   ## IV. Value Objectives
   Helps model providers and users achieve new business growth and builds a commercial win-win model within the large model ecosystem.
   ```



</div>
</div>


```mixin-react
return (<Tabs>
<Tabs.TabPane title="Curl" key="bOeMSgWy5j"><RenderMd content={`\`\`\`Bash
curl https://ark.ap-southeast.bytepluses.com/api/v3/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer $ARK_API_KEY" \\
  -d '{
    "model": "seed-2-0-lite-260228",
    "messages": [
        {"role": "user", "content": "Please structurally organize the following content: ModelArk is a large model service platform launched by BytePlus. It provides comprehensive functions and services such as model training, inference, evaluation, and fine-tuning, and focuses on supporting the large model ecosystem. Through stable and reliable secure mutual trust solutions, ModelArk ensures the model security of model providers and the information security of model users, accelerates the penetration of large model capabilities into various industries, and helps model providers and users achieve new business growth."}
    ],
     "thinking":{
         "type":"disabled"
     }
  }'
\`\`\`


* Replace the Model ID as needed. To query the Model ID, see the [Model list](/docs/ModelArk/1330310).
`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="Python" key="flgkMG5ppw"><RenderMd content={`\`\`\`Python
import os
# Install SDK:  pip install byteplus-python-sdk-v2 
from byteplussdkarkruntime import Ark 

# Initialize Ark Client
client = Ark(
    # The base URL for model invocation
    base_url="https://ark.ap-southeast.bytepluses.com/api/v3", 
    # Get API Key：https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey
    api_key=os.getenv('ARK_API_KEY'), 
)

completion = client.chat.completions.create(
    # Replace with Model ID
    model = "seed-2-0-lite-260228",
    messages=[
        {"role": "user", "content": "Please structurally organize the following content: ModelArk is a large model service platform launched by BytePlus. It provides comprehensive functions and services such as model training, inference, evaluation, and fine-tuning, and focuses on supporting the large model ecosystem. Through stable and reliable secure mutual trust solutions, ModelArk ensures the model security of model providers and the information security of model users, accelerates the penetration of large model capabilities into various industries, and helps model providers and users achieve new business growth."},
    ],
    # thinking={"type": "disabled"}, #  Manually disable deep thinking
)
print(completion.choices[0].message.content)
\`\`\`

`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="Go" key="lTZhsfPheo"><RenderMd content={`\`\`\`Go
package main

import (
    "context"
    "fmt"
    "os"
    "github.com/byteplus-sdk/byteplus-go-sdk-v2/service/arkruntime"
    "github.com/byteplus-sdk/byteplus-go-sdk-v2/service/arkruntime/model"
    "github.com/byteplus-sdk/byteplus-go-sdk-v2/byteplus"
)

func main() {
    client := arkruntime.NewClientWithApiKey(
        os.Getenv("ARK_API_KEY"),
        // The base URL for model invocation
        arkruntime.WithBaseUrl("https://ark.ap-southeast.bytepluses.com/api/v3"),
    )
    
    ctx := context.Background()
    req := model.CreateChatCompletionRequest{
        // Replace with Model ID
       Model: "seed-2-0-lite-260228",
       Messages: []*model.ChatCompletionMessage{
          {
             Role: model.ChatMessageRoleUser,
             Content: &model.ChatCompletionMessageContent{
                StringValue: byteplus.String("Please structurally organize the following content: ModelArk is a large model service platform launched by BytePlus. It provides comprehensive functions and services such as model training, inference, evaluation, and fine-tuning, and focuses on supporting the large model ecosystem. Through stable and reliable secure mutual trust solutions, ModelArk ensures the model security of model providers and the information security of model users, accelerates the penetration of large model capabilities into various industries, and helps model providers and users achieve new business growth."),
             },
          },
       },
       Thinking: &model.Thinking{
            Type: model.ThinkingTypeDisabled, // Manually disable deep thinking
            // Type: model.ThinkingTypeEnabled, // Manually enable deep thinking
        },
    }

    resp, err := client.CreateChatCompletion(ctx, req)
    if err != nil {
       fmt.Printf("standard chat error: %v\n", err)
       return
    }
    fmt.Println(*resp.Choices[0].Message.Content.StringValue)
}
\`\`\`

`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="Java" key="jF75ffZrf8"><RenderMd content={`\`\`\`java
package com.ark.sample;

import com.byteplus.ark.runtime.model.completion.chat.*;
import com.byteplus.ark.runtime.service.ArkService;
import java.util.ArrayList;
import java.util.List;

public class ChatCompletionsExample {
    public static void main(String[] args) {
        String apiKey = System.getenv("ARK_API_KEY");
        // The base URL for model invocation
        ArkService service = ArkService.builder().apiKey(apiKey).baseUrl("https://ark.ap-southeast.bytepluses.com/api/v3").build();
        final List<ChatMessage> messages = new ArrayList<>();
        final ChatMessage userMessage = ChatMessage.builder().role(ChatMessageRole.USER).content("Please structurally organize the following content: ModelArk is a large model service platform launched by Volcano Engine. It provides comprehensive functions and services such as model training, inference, evaluation, and fine-tuning, and focuses on supporting the large model ecosystem. Through stable and reliable secure mutual trust solutions, ModelArk ensures the model security of model providers and the information security of model users, accelerates the penetration of large model capabilities into various industries, and helps model providers and users achieve new business growth.").build();
        messages.add(userMessage);

        ChatCompletionRequest chatCompletionRequest = ChatCompletionRequest.builder()
               .model("seed-2-0-lite-260228")//Replace with Model ID
               .messages(messages)
               // .thinking(new ChatCompletionRequest.ChatCompletionRequestThinking("disabled")) // Manually disable deep thinking
               .build();
        service.createChatCompletion(chatCompletionRequest).getChoices().forEach(choice -> System.out.println(choice.getMessage().getContent()));
        // shutdown service
        service.shutdownExecutor();
    }
}
\`\`\`

`}></RenderMd></Tabs.TabPane></Tabs>);
 ```

<span id="04e3872d"></span>
# Models and APIs
Supported models: [Text generation](/docs/ModelArk/1330310#b318deb2)
Supported APIs:

* <a href="https://docs.byteplus.com/en/docs/ModelArk/Create_model_request">Responses API</a>: A newly launched API with concise context management, enhanced tool calling , and reduced costs through caching, recommended for new businesses and new users.
* <a href="https://docs.byteplus.com/en/docs/ModelArk/Chat">Chat API</a>: Widely used API that makes it easy and cost-effective to migrate existing business applications.

<span id="9f37c3d7"></span>
# Samples
<span id="9ba76a58"></span>
## Multi-turn conversation
To implement multi-turn conversation, the conversation history, which includes system messages, model messages, and user messages, must be combined into a list so that the model can understand the context and continue the conversation on previous topics.

<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.1504912832929782);">

**Input method**


</div>
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.5379004842615012);margin-left: 16px;">

**Manually manage context**


</div>
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.31150823244552056);margin-left: 16px;">

**Manage context via ID**


</div>
</div>


---



<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.1504912832929782);">

Sample


</div>
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.5366898305084745);margin-left: 16px;">

```JSON
...
    "model": "seed-2-0-lite-260228",
    "messages":[
        {"role": "user", "content": "Hi, tell a joke."},
        {"role": "assistant", "content": "Why did the math book look sad? Because it had too many problems! 😄"},
        {"role": "user", "content": "What's the punchline of this joke?"}
    ]
...
```



</div>
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.3127188861985472);margin-left: 16px;">

```Plain Text
...
    "model": "seed-2-0-lite-260228",
    "previous_response_id":"<id>",
    "input": "What is the punchline of this joke?"    
...
```




</div>
</div>


<div style="display: flex;">
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.1504912832929782);">

API


</div>
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.5366898305084745);margin-left: 16px;">

<a href="https://docs.byteplus.com/en/docs/ModelArk/Chat">Chat API</a>


</div>
<div style="flex-shrink: 0;width: calc((100% - 32px) * 0.3127188861985472);margin-left: 16px;">

<a href="https://docs.byteplus.com/en/docs/ModelArk/Create_model_request">Responses API</a>


</div>
</div>

<span id="38da7705"></span>
## Streaming output
Advantages:

* **Improved waiting experience:** No need to wait for the entire content to be generated; you can process the content as it's being generated.
* **Real-time feedback:** In multi-turn interaction scenarios, you can understand the current stage of the task in real-time.
* **Higher fault tolerance:** Even if an error occurs midway, you can still obtain the content that has already been generated, avoiding the situation where non-streaming output fails and returns nothing.
* **Simplified timeout management:** Maintain the connection status between the client and the server, preventing connection timeouts due to overly long processing times for complex tasks.

Enable streaming output by setting **stream** to `true`.
```JSON
...
    "model": "seed-2-0-lite-260228",
    "messages": [
        {"role": "user", "content": "What is the difference between a deep thinking model and a non-deep thinking model?"}
    ],
    "stream": true
 ...
```

<span id="2fa62a85"></span>
## Setting the maximum response length
To control costs or response time, you can limit the model's response length. When the response is lengthy, such as translating long texts, to avoid being truncated midway, you can set a larger value for `max_tokens`.
```JSON
...
    "model": "seed-2-0-lite-260228",
    "messages": [
        {"role": "user","content": "What are some common cruciferous plants?"}
    ],
    "max_tokens": 300
...
```

<span id="3c1d6c46"></span>
## Asynchronous output
In scenarios involving complex tasks or concurrent tasks, you can use the Asyncio interface to implement concurrent calls, improving program efficiency and optimizing the user experience.

* Chat API code example:
   
   ```mixin-react
   return (<Tabs>
   <Tabs.TabPane title="Python" key="kLPIL6rAeY"><RenderMd content={`\`\`\`Python
   import asyncio
   import os
   # Install SDK:  pip install byteplus-python-sdk-v2 
   from byteplussdkarkruntime import AsyncArk
   
   # Initialize Ark Client
   client = AsyncArk(
       # The base URL for model invocation
       base_url="https://ark.ap-southeast.bytepluses.com/api/v3", 
       # Get API Key：https://console.byteplus.com/ark/region:ark+ap-southeast-1/apikey 
       api_key=os.getenv('ARK_API_KEY'), 
   )
   
   async def main() -> None:
       stream = await client.chat.completions.create(  
           # Replace with Model ID
           model = "seed-2-0-lite-260228",
           messages=[
               {"role": "system", "content": "You are an AI assistant."},
               {"role": "user", "content": "What are some common cruciferous plants?"},
           ],
           stream=True
       )
       async for completion in stream:
           print(completion.choices[0].delta.content, end="")
       print()
       
   if __name__ == "__main__":
       asyncio.run(main())
   \`\`\`
   
   `}></RenderMd></Tabs.TabPane></Tabs>);
    ```

* Response API code example:
   
   ```mixin-react
   return (<Tabs>
   <Tabs.TabPane title="Python" key="g1WxLRRyOx"><RenderMd content={`\`\`\`Python
   import asyncio
   import os
   from byteplussdkarkruntime import AsyncArk 
   from byteplussdkarkruntime.types.responses.response_completed_event import ResponseCompletedEvent
   from byteplussdkarkruntime.types.responses.response_reasoning_summary_text_delta_event import ResponseReasoningSummaryTextDeltaEvent
   from byteplussdkarkruntime.types.responses.response_output_item_added_event import ResponseOutputItemAddedEvent
   from byteplussdkarkruntime.types.responses.response_text_delta_event import ResponseTextDeltaEvent
   from byteplussdkarkruntime.types.responses.response_text_done_event import ResponseTextDoneEvent
   
   
   client = AsyncArk(
       base_url='https://ark.ap-southeast.bytepluses.com/api/v3',
       api_key=os.getenv('ARK_API_KEY')
   )
   
   async def main():
       stream = await client.responses.create(
           model="seed-2-0-lite-260228",
           input=[
               {"role": "system", "content": "You are an AI assistant."},
               {"role": "user", "content": "What are some common cruciferous plants?"},
           ],
           stream=True
       )
       async for event in stream:
           if isinstance(event, ResponseReasoningSummaryTextDeltaEvent):
               print(event.delta, end="")
           if isinstance(event, ResponseOutputItemAddedEvent):
               print("\noutPutItem " + event.type + " start:")
           if isinstance(event, ResponseTextDeltaEvent):
               print(event.delta,end="")
           if isinstance(event, ResponseTextDoneEvent):
               print("\noutPutTextDone.")
           if isinstance(event, ResponseCompletedEvent):
               print("Response Completed. Usage = " + event.response.usage.model_dump_json())
   
   
   if __name__ == "__main__":
       asyncio.run(main())
   \`\`\`
   
   `}></RenderMd></Tabs.TabPane></Tabs>);
    ```


<span id="762913a1"></span>
# Tips
<span id="2991881d"></span>
## Deep thinking
Before generating an answer, the model first performs a systematic analysis and logical breakdown of the input question, and then generates the answer based on the breakdown results. This can significantly improve the quality of the responses, but it will increase token consumption. For more details, see [Deep reasoning](/docs/ModelArk/1449737).
<span id="bf6bcba4"></span>
## Prompt engineering
Properly designing and writing prompts, such as providing instructions, examples, and good guidelines, can improve the quality and accuracy of the model's output. This process of optimizing prompts is also known as prompt engineering. For more details, see [Prompt engineering](/docs/ModelArk/1221660).
<span id="c0bb9ad0"></span>
## Tools
By integrating built-in tools or connecting to remote MCP servers, you can extend the model's capabilities to better answer questions or perform tasks. Currently supported:

* Built-in tools: Web Search, Knowledge Search, Image Process, etc.
* Function calling.
* Third-party MCP services.

<span id="3d405f12"></span>
## Prefill response mode
By prefilling parts of the **assistant** role's content, this mode guides and controls the model to continue generating output based on existing text fragments, and also helps maintain consistency in role-playing scenarios.

* [Prefill-based response](/docs/ModelArk/1359497): implemented with the <a href="https://docs.byteplus.com/en/docs/ModelArk/Chat">Chat API</a>.

<span id="cbdfe3bc"></span>
## Structured output (beta)
Control the model's output to generate a standardized format (primarily JSON) instead of natural language, making it easier to standardize processing or display.

* [Structured output (beta)](/docs/ModelArk/1568221): implemented with the <a href="https://docs.byteplus.com/en/docs/ModelArk/Chat">Chat API</a>.

<span id="6bb67fe5"></span>
## Batch inference
ModelArk provides batch inference capabilities. When you have large-scale data processing tasks, you can use batch inference to achieve higher throughput and lower costs. For detailed information and usage, see [Batch inference](/docs/ModelArk/1399517).
<span id="574d4650"></span>
## Exception handling
Add exception handling to help pinpoint issues.

```mixin-react
return (<Tabs>
<Tabs.TabPane title="Python" key="OAmUeU2A9s"><RenderMd content={`\`\`\`Python
import os
# Install SDK:  pip install byteplus-python-sdk-v2 
from byteplussdkarkruntime import Ark
from byteplussdkarkruntime._exceptions import ArkAPIError

# Initialize Ark Client
client = Ark(
    # The base URL for model invocation
    base_url="https://ark.ap-southeast.bytepluses.com/api/v3",    
    api_key=os.getenv('ARK_API_KEY'), 
)

# Streaming
try:
    stream = client.chat.completions.create(
    # Replace with Model ID
    model = "seed-2-0-lite-260228",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": "What are some common cruciferous plants?"},
        ],
        stream=True
    )
    for chunk in stream:
        if not chunk.choices:
            continue

        print(chunk.choices[0].delta.content, end="")
    print()
except ArkAPIError as e:
    print(e)
\`\`\`

`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="Go" key="dbs2xgNVIb"><RenderMd content={`\`\`\`Go
package main

import (
    "context"
    "errors"
    "fmt"
    "io"
    "os"
    "github.com/byteplus-sdk/byteplus-go-sdk-v2/service/arkruntime"
    "github.com/byteplus-sdk/byteplus-go-sdk-v2/service/arkruntime/model"
    "github.com/byteplus-sdk/byteplus-go-sdk-v2/byteplus"
)

func main() {
    client := arkruntime.NewClientWithApiKey(
        os.Getenv("ARK_API_KEY"),
        // The base URL for model invocation
        arkruntime.WithBaseUrl("https://ark.ap-southeast.bytepluses.com/api/v3"),
    )
    ctx := context.Background()

    fmt.Println("----- streaming request -----")
    req := model.CreateChatCompletionRequest{
        // Replace with Model ID
       Model: "seed-2-0-lite-260228",
       Messages: []*model.ChatCompletionMessage{
          {
             Role: model.ChatMessageRoleSystem,
             Content: &model.ChatCompletionMessageContent{
                StringValue: byteplus.String("You are an AI assistant."),
             },
          },
          {
             Role: model.ChatMessageRoleUser,
             Content: &model.ChatCompletionMessageContent{
                StringValue: byteplus.String("What are some common plants in the Brassicaceae family?"),
             },
          },
       },
    }
    stream, err := client.CreateChatCompletionStream(ctx, req)
    if err != nil {
       apiErr := &model.APIError{}
       if errors.As(err, &apiErr) {
          fmt.Printf("stream chat error: %v\n", apiErr)
       }
       return
    }
    defer stream.Close()

    for {
       recv, err := stream.Recv()
       if err == io.EOF {
          return
       }
       if err != nil {
          apiErr := &model.APIError{}
          if errors.As(err, &apiErr) {
             fmt.Printf("stream chat error: %v\n", apiErr)
          }
          return
       }

       if len(recv.Choices) > 0 {
          fmt.Print(recv.Choices[0].Delta.Content)
       }
    }
}
\`\`\`

`}></RenderMd></Tabs.TabPane>
<Tabs.TabPane title="Java" key="aMG4XE4Aks"><RenderMd content={`\`\`\`java
package com.volcengine.ark.runtime;

import com.byteplus.ark.runtime.exception.ArkHttpException;
import com.byteplus.ark.runtime.model.completion.chat.ChatCompletionRequest;
import com.byteplus.ark.runtime.model.completion.chat.ChatMessage;
import com.byteplus.ark.runtime.model.completion.chat.ChatMessageRole;
import com.byteplus.ark.runtime.service.ArkService;
import java.util.ArrayList;
import java.util.List;


public class ChatCompletionsExample {
    public static void main(String[] args) {

        String apiKey = System.getenv("ARK_API_KEY");
        // The base URL for model invocation
        ArkService service = ArkService.builder().apiKey(apiKey).baseUrl("https://ark.ap-southeast.bytepluses.com/api/v3").build();

        System.out.println("----- streaming request -----");
        final List<ChatMessage> streamMessages = new ArrayList<>();
        final ChatMessage streamSystemMessage = ChatMessage.builder().role(ChatMessageRole.SYSTEM).content("You are an AI assistant.").build();
        final ChatMessage streamUserMessage = ChatMessage.builder().role(ChatMessageRole.USER).content("What are some common plants in the Brassicaceae family?").build();
        streamMessages.add(streamSystemMessage);
        streamMessages.add(streamUserMessage);

        ChatCompletionRequest streamChatCompletionRequest = ChatCompletionRequest.builder()
               .model("seed-2-0-lite-260228")//Replace with Model ID
               .messages(streamMessages)
               .build();

        try {
            service.streamChatCompletion(streamChatCompletionRequest)
                   .doOnError(Throwable::printStackTrace)
                   .blockingForEach(
                            choice -> {
                                if (choice.getChoices().size() > 0) {
                                    System.out.print(choice.getChoices().get(0).getMessage().getContent());
                                }
                            }
                    );
        } catch (ArkHttpException e) {
            System.out.print(e.toString());
        }

        // shutdown service
        service.shutdownExecutor();
    }

}
\`\`\`

`}></RenderMd></Tabs.TabPane></Tabs>);
 ```

<span id="c2a850b4"></span>
## Conversation encryption
In addition to the default network layer encryption, ModelArk also provides free application layer encryption, providing stronger security for your inference session data. You only need to add one line of code to enable it. For a complete code example, see [Data encryption](/docs/ModelArk/1544136#23274b89); for further information, see [Inferential Session Data Application Layer Encryption Scheme](/docs/ModelArk/1389905).
<span id="f2a89e72"></span>
# Usage instructions

* Key limitations of models:
   * Context window: This refers to the amount of content a model can process in a single request, including user input and model output, measured in tokens. If the content exceeds the context window, it will be truncated and output will stop. If you encounter content truncation due to context limitations, you can choose a model with a larger context window.
   * Max tokens: This refers to the maximum length of the content that the model can output in a single response. If you encounter this limitation, you can refer to [Prefill-based response](/docs/ModelArk/1359497) and use multiple continuations to piece together the complete content.
   * Tokens Per Minute (TPM): This refers to the maximum amount of content that a model (regardless of version) can process per minute for an account, measured in tokens. If the default TPM limit does not meet your business needs, you can contact customer support by creating a [Ticket](https://console.byteplus.com/workorder/create?step=2&SubProductID=P00001514) to increase your quota. For example, if a model has a TPM of 5 million, all versions of that model created under a main account share this quota.
   * Requests Per Minute (RPM): This refers to the maximum number of requests that a model (regardless of version) can process per minute for an account. This is similar to TPM. If the default RPM limit does not meet your business needs, you can contact customer support by creating a [Ticket](https://console.byteplus.com/workorder/create?step=2&SubProductID=P00001514) to increase your quota.
   * For detailed specifications of each model, see [Model list](/docs/ModelArk/1330310).
* Usage query:
   * Token usage for a specific request: You can view it in the returned **usage** object.
   * Token usage for input/output: You can calculate or estimate with <a href="https://docs.byteplus.com/en/docs/ModelArk/tokenization">Tokenization API</a> or [Token Calculator](https://console.byteplus.com/ark/region:ark+ap-southeast-1/tokenCalculator).
   * Token usage by account, project, and endpoint: You can view it on the [Usage](https://console.byteplus.com/ark/region:ark+ap-southeast-1/usageTracking) page of the console.

<span id="e5555ae5"></span>
# FAQ
For FAQs about online inference, see [Online inference](/docs/ModelArk/1359411#aa45e6c0). If you encounter any issue, you can try to find solutions in this document.
