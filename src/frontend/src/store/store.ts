// import { devtools, persist } from "zustand/middleware";
import { ChatStoreState, Convo, InputPrompt } from "./types"
import { create } from "zustand"

const useChatStore = create<ChatStoreState>()((set) => ({
	convos: [],
	inputPrompts: [],

	addConvos: (newConvos: Convo[]) => {
		set((state) => {
			const convoIds = new Set(state.convos.map((convo) => convo.id))
			const uniqueConvos = newConvos.filter(
				(newConvo) => !convoIds.has(newConvo.id)
			)
			const sortedConvos = [...state.convos, ...uniqueConvos].sort(
				(a, b) =>
					new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
			)
			return {
				convos: sortedConvos,
			}
		})
	},

	deleteConvo: (id: number) => {
		set((state) => ({
			convos: state.convos.filter((convo) => convo.id !== id),
		}))
	},

	renameConvo: (id: number, newName: string) => {
		set((state) => {
			const updatedConvos = state.convos.map((convo) =>
				convo.id === id ? { ...convo, title: newName } : convo
			)
			return {
				convos: updatedConvos,
			}
		})
	},

	archiveConvo: (id: number) => {
		set((state) => {
			const updatedConvos = state.convos.map((convo) =>
				convo.id === id ? { ...convo, archived: true } : convo
			)
			return {
				convos: updatedConvos,
			}
		})
	},

	unarchiveConvo: (id: number) => {
		set((state) => {
			const updatedConvos = state.convos.map((convo) =>
				convo.id === id ? { ...convo, archived: false } : convo
			)
			return {
				convos: updatedConvos,
			}
		})
	},

	updateInputPrompts: (newInputPrompts: InputPrompt[]) => {
		set((state) => {
			const promptIds = new Set(state.inputPrompts.map((prompt) => prompt.id))
			const uniqueInputPrompts = newInputPrompts.filter(
				(newInputPrompts) => !promptIds.has(newInputPrompts.id)
			)
			const sortedPrompts = [...state.inputPrompts, ...uniqueInputPrompts].sort(
				(a, b) =>
					new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
			)
			return {
				inputPrompts: sortedPrompts,
			}
		})
	},
	setInputPrompts: (newInputPrompts: InputPrompt[]) => {
		set(() => {
			return {
				inputPrompts: newInputPrompts,
			}
		})
	},
}))

export default useChatStore
