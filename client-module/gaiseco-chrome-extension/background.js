console.log("DEBUG FROM background");


async function loadConfigData() {
    const response = await fetch('./config.json', {});
    // .then(response => response.json())
    // .then(json => console.log(json);
    readFile = await response.json();

    return readFile;
};



function filterChatPayload(requestBody, url) {
    let content = {};

    if (url.includes('deepseek')) {
        // Do bufferArray de bytes, decodificando para string e por fim passando para JSON.
        const bufferArray = requestBody.raw[0].bytes;
        const requestPayload = new TextDecoder().decode(bufferArray);
        const payload = JSON.parse(requestPayload.toString());

        content.source = "deepseek";
        content.model = "r1";
        content.session = payload.chat_session_id;
        content.prompt = payload.prompt;
    } else if (url.includes('grok')) {
        // Do bufferArray de bytes, decodificando para string e por fim passando para JSON.
        const bufferArray = requestBody.raw[0].bytes;
        const requestPayload = new TextDecoder().decode(bufferArray);
        const payload = JSON.parse(requestPayload.toString());

        content.source = "grok";
        content.model = payload.modelName;
        content.session = url;
        content.prompt = payload.message;
    } else if (url.includes('chatgpt')) {
        // Do bufferArray de bytes, decodificando para string e por fim passando para JSON.
        const bufferArray = requestBody.raw[0].bytes;
        const requestPayload = new TextDecoder().decode(bufferArray);
        const payload = JSON.parse(requestPayload.toString());

        content.source = "chatgpt";
        content.model = payload.model;
        content.session = payload.conversation_id;
        content.prompt = payload.messages[0].content.parts.toString();
    } else if (url.includes('gemini')) {
        // Do bufferArray de bytes, decodificando para string e por fim passando para JSON.
        const requestPayload = requestBody.formData["f.req"][0];

        content.source = "gemini";
        content.model = "bard";
        content.session = url;
        content.prompt = requestPayload.split("[[\\\"")[1].split("\\\",0,null,null,null,null,0]")[0].toString();
    } else if (url.includes('perplexity')) {
        // Do bufferArray de bytes, decodificando para string e por fim passando para JSON.
        const bufferArray = requestBody.raw[0].bytes;
        const requestPayload = new TextDecoder().decode(bufferArray);
        const payload = JSON.parse(requestPayload.toString());

        content.source = "perplexity";
        content.model = "";
        content.session = url;
        content.prompt = payload.query_str.toString();
    }

    return content;
}


chrome.webRequest.onBeforeRequest.addListener(async (details) => {
    // console.log(details.requestBody);


    const payloadDataFiltered = filterChatPayload(details.requestBody, details.url);

    console.log(payloadDataFiltered);
    console.log(details.url);

    const configData = await loadConfigData();
    console.log(configData);

    // Unindo os dois JSON obj.
    const chatData = { ...configData, ...payloadDataFiltered };


    // Enviando para o servidor
    const response = await fetch(configData.server_address + 'check', {
        method: 'POST',
        headers: {
            'User-Agent': 'service-worker',
            'Content-Type': 'application/json;charset=UTF-8',
        },
        body: JSON.stringify(chatData),
    });
},
    {
        urls: [
            "https://chat.deepseek.com/api/v0/chat/completion",
            "https://grok.com/rest/app-chat/conversations/*",
            "https://chatgpt.com/backend-api/conversation",
            "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/*",
            "https://www.perplexity.ai/rest/sse/perplexity_ask"
        ]
    },
    ["requestBody"]
);

