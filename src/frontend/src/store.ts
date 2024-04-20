import { create } from "zustand";

import { devtools, persist } from "zustand/middleware";

interface Convo {
    id: number;
    assitant_id: string;
    title: string;
    created_at: string;
    Archive_convo: boolean;
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
    renameConvo: (id: number, newtitle: string) => {
        set((state) => ({
            convos: state.convos.map((convo) =>
                convo.id === id ? { ...convo, title: newtitle } : convo,
            ),
        }));
    },

    updateInputPrompt: (text_query: string, response_text: string) => {},

    deleteConvo: (id: number) => {
        set((state) => ({
            convos: state.convos.filter((convo) => convo.id !== id),
        }));
    },

    getConvo: (id: number) => {
        return chatStore.getState().convos.find((convo) => convo.id === id);
    },

    archiveConvo: (id: number) => {
        set((state) => ({
            convos: state.convos.map((convo) =>
                convo.id === id ? { ...convo, Archive_convo: true } : convo,
            ),
        }));
    },
}));

const useChatStore = create(
    devtools(
        persist(chatStore, {
            name: "chat-store",
        }),
    ),
);

export default useChatStore;
