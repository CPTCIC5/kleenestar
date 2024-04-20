import {ChatStoreState } from '../types'
import {create} from 'zustand'




const chatStore = create<ChatStoreState>((set) => ({
	convos: [],
	inputPrompts: [],
	renameConvo: (id: number, newtitle: string) => {
		set((state) => ({
			convos: state.convos.map((convo) =>
				convo.id === id ? { ...convo, title: newtitle } : convo
			),
		}))
	},

	updateInputPrompt: (text_query: string, response_text: string) => {},

	deleteConvo: (id: number) => {
		set((state) => ({
			convos: state.convos.filter((convo) => convo.id !== id),
		}))
	},

	getConvo: (id: number) => {
		return chatStore.getState().convos.find((convo) => convo.id === id)
	},
	
	archiveConvo: (id: number) => {
		set((state) => ({
			convos: state.convos.map((convo) =>
				convo.id === id ? { ...convo, Archive_convo: true } : convo
			),
		}))
	},
}))


export default chatStore