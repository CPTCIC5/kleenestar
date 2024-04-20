import { create } from "zustand";
import chatStore from './store/chat/index'
import { devtools, persist } from "zustand/middleware";






const useChatStore = create(
    devtools(
        persist(chatStore, {
            name: "chat-store",
        }),
    ),
);

export default useChatStore;
