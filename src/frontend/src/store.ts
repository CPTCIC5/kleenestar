import { create } from "zustand";

import { devtools, persist } from "zustand/middleware";

interface Convo {
    id: number;
    assitant_id: string;
    title: string;
    created_at: string;
}

interface InputPrompt {
    id: number;
    convo_id: number;
    author: string;
    text_query: string;
    file_query: string;
    response_text: string;
    response_image: string;
    created_at: string;
}

interface ChatStoreState {
    convos: Convo[];
    inputPrompts: InputPrompt[];
}

const chatStore = create<ChatStoreState>((set) => ({
    convos: [],
    inputPrompts: [],
    
}));

const useChatStore = create(
    devtools(
        persist(chatStore, {
            name: "chat-store",
        }),
    ),
);

export default useChatStore;
