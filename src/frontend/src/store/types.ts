interface Convo {
	id: number
	assitant_id: string
	title: string
	created_at: string
	Archive_convo: boolean
}

interface InputPrompt {
	id: number
	convo_id: number
	author: string
	text_query: string
	file_query: string
	response_text: string
	response_image: string
	created_at: string
}

interface ChatStoreState {
	convos: Convo[]
	inputPrompts: InputPrompt[]
}


export type { Convo, InputPrompt, ChatStoreState }