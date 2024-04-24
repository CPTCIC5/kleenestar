interface Convo {
    id: number;
    assitant_id: string;
    workspace: object;
    title: string;
    created_at: string;
    archived: boolean;
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
	convos: Convo[]
	inputPrompts: InputPrompt[]
	addConvos: (newConvos: Convo[]) => void
	deleteConvo: (id: number) => void
	renameConvo: (id: number, newName: string) => void
	archiveConvo: (id: number) => void
	unarchiveConvo: (id: number) => void
	updateInputPrompts: (newInputPrompts: InputPrompt[]) => void
	setInputPrompts: (newInputPrompts: InputPrompt[]) => void
}

export type { Convo, InputPrompt, ChatStoreState };
