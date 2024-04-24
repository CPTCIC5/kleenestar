import {
	ArchiveRestore,
	CircleHelp,
	Clipboard,
	ImageUp,
	SendHorizonal,
	SquareMenuIcon,
	X,
} from "lucide-react"
import React, { useEffect, useRef, useState } from "react"
import NewChatDisplay from "./NewChatDisplay"
import { InputPrompt } from "../utils/dummyChatData"
import axios from "axios"
import Cookies from "js-cookie"
import useChatStore from "../store/store"
import { toast } from "sonner"

interface ChatDisplayProps {
	handleHide: () => void
	currentConvoId: number
	isOpenArchive: boolean
	onCloseArchive: (option: boolean) => void
}

const ChatDisplay: React.FC<ChatDisplayProps> = ({
	handleHide,
	currentConvoId,
	isOpenArchive,
	onCloseArchive,
}) => {
	const updateInputPrompts = useChatStore((state) => state.updateInputPrompts)
    const setInputPrompts = useChatStore((state) => state.setInputPrompts)
	const inputPrompts = useChatStore((state) => state.inputPrompts)
	const convos = useChatStore((state) => state.convos)
	const renameConvo = useChatStore((state) => state.renameConvo)
	const [Data, setData] = useState(InputPrompt)
	const [text, setText] = useState("")
	const [isEditing, setIsEditing] = useState<boolean>(false)
	const [buttonText, setButtonText] = useState<string>("New Chat")
	const [newName, setNewName] = useState<string>("")
	const [uploadedFiles, setUploadedFiles] = useState<string | null>(null)
	const fileInputRef = useRef<HTMLInputElement>(null)

	const sendMessage = async () => {
		console.log(text, uploadedFiles)
		const inputText: string = text
		setText("")
		if (!text) {
			toast.warning("Please enter your message")
			return
		} else {
			try {
				//creates input prompt in the backend
                inputPrompts.push({
									id: 0,
									convo_id: 0,
									author: "",
									text_query: inputText,
									file_query: "",
									response_text: "thinking...",
									response_image: "",
									created_at: "",
								})
				await axios.post(
					`http://127.0.0.1:8000/api/channels/convos/${currentConvoId}/prompts/create/`,
					{
						text_query: inputText,
						file_query: uploadedFiles,
					},
					{
						withCredentials: true,
						headers: {
							"Content-Type": "application/json",
							"X-CSRFToken": Cookies.get("csrftoken"),
						},
					}
				)
				const response = await axios.get(
					`http://127.0.0.1:8000/api/channels/convos/${currentConvoId}/prompts/`,
					{
						withCredentials: true,
						headers: {
							"Content-Type": "application/json",
							"X-CSRFToken": Cookies.get("csrftoken"),
						},
					}
				)
				console.log(response)
                inputPrompts.pop()
				updateInputPrompts(response.data.results)
			} catch (err) {
				console.error(err)
			}
		}
	}

	const handleUploadClick = () => {
		fileInputRef.current?.click()
	}

	const handleUploadFileChange = (
		event: React.ChangeEvent<HTMLInputElement>
	) => {
		if (event.target.files) {
			setUploadedFiles(URL.createObjectURL(event.target.files[0]))
		}
	}

	const handleRemoveFile = () => {
		setUploadedFiles(null)
	}

	const handleRenameChat = async (id: number, newName: string) => {
		try {
			await axios.patch(
				`http://127.0.0.1:8000/api/channels/convos/${id}/`,
				{
					title: newName,
				},
				{
					withCredentials: true,
					headers: {
						"Content-Type": "application/json",
						"X-CSRFToken": Cookies.get("csrftoken"),
					},
				}
			)
			renameConvo(id, newName)
			console.log(convos)
		} catch (error) {
			console.error(error)
		}
	}
    useEffect(() => {
        const updatePrompts = async() => {
            const response = await axios.get(
                `http://127.0.0.1:8000/api/channels/convos/${currentConvoId}/prompts/`,
                {
                    withCredentials: true,
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": Cookies.get("csrftoken"),
                    },
                }
            )
            console.log(response.data.results)
            setInputPrompts(response.data.results)
            
        }
		updatePrompts();
			
		}, [currentConvoId, updateInputPrompts])

	const handleClick = () => {
		if (isEditing) {
			if (newName.trim() !== "") {
				setButtonText(newName)
				handleRenameChat(currentConvoId, newName)
			}
			setIsEditing(false)
		} else {
			setIsEditing(true)
			setNewName(buttonText)
		}
	}

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		setNewName(e.target.value)
	}

	const handleBlur = () => {
		handleClick()
	}

	return (
		<div className="h-screen w-full  flex flex-col relative justify-between flex-1">
			<div className="w-full h-[56px] mb-[6px] p-[8px] px-[15px] flex justify-between items-center">
				<SquareMenuIcon
					onClick={handleHide}
					className="w-[25px] h-[25px] text-primary-300"
				/>
				<div className="overflow-hidden h-[56px] w-full mx-[30px]">
					{isEditing ? (
						<input
							type="text"
							className="outline-none border-none mx-[10px] font-syne font-bold text-[15px] text-center text-primary-300 bg-inherit w-full h-full"
							value={newName}
							onChange={handleChange}
							onBlur={handleBlur}
							onKeyPress={(event) => {
								if (event.key === "Enter") {
									event.preventDefault()
									handleBlur()
								}
							}}
							autoFocus
						/>
					) : (
						<button
							className="outline-none border-none mx-[10px] font-syne font-bold text-[15px] text-primary-300 bg-inherit w-full overflow-hidden whitespace-nowrap overflow-ellipsis h-full"
							onClick={handleClick}>
							{buttonText}
						</button>
					)}
				</div>
				<ArchiveRestore
					onClick={() => onCloseArchive(isOpenArchive)}
					className="w-[25px] h-[25px] text-primary-300"
				/>
			</div>
			{/* Chat Header */}
			<section className="w-full h-full flex flex-col items-center px-[8px]   overflow-auto">
				<div className="max-w-[755.7px] w-full h-full  ">
					{inputPrompts.length === 0 ? (
						<NewChatDisplay />
					) : (
						<div className="w-full flex flex-col justify-center gap-[40px]">
							{inputPrompts.map((item, index) => {
								return (
									<div
										key={index}
										className="flex flex-col gap-[40.84px]">
										<div className="flex gap-[22.36px]">
											<img
												src="/group-2085-user.svg"
												alt=""
											/>
											<div>
												<span className="font-montserrat font-[400] text-[16px] leading-[19.5px] text-primary-300">
													{item?.text_query}
												</span>
											</div>
										</div>
										<div className="flex gap-[22.36px] items-start">
											<img
												src="/group-2085-bot.svg"
												alt=""
											/>
											<div className="flex flex-col gap-[16px]">
												<span className="font-montserrat font-[400] text-[16px] leading-[19.5px] text-primary-300">
													{item?.response_text}
												</span>
												<Clipboard className="w-[20px] h-[20px] bg-transparent text-primary-200" />
											</div>
										</div>
									</div>
								)
							})}
						</div>
					)}
				</div>
			</section>
			{/* Chat Bottom */}
			<div className="w-full flex flex-col gap-[16.39px] items-center p-[16px] pt-[6px] mt-[10px]">
				<div
					className="relative flex flex-col justify-center item-center max-w-[776.62px] w-full h-full min-h-[52px] outline-2 outline outline-primary-200 focus:outline-primary-200  focus:outline rounded-3xl  focus:outline-none
                ">
					{uploadedFiles && (
						<div className="px-[15.02px] py-[12.26px] w-[200px] h-[150px] overflow-hidden">
							<div className="relative w-full h-full">
								<img
									src={uploadedFiles}
									alt="uploaded file"
									className="object-cover w-full h-full rounded-2xl"
								/>
								<button
									className="absolute top-2 right-2 p-[3px] py-[4px] rounded-full justify-center items-center flex"
									onClick={handleRemoveFile}>
									<span className="text-primary-300 h-[15px] w-[18px] text-[18px] font-medium font-montserrat flex justify-center items-center">
										<X />
									</span>
								</button>
							</div>
						</div>
					)}
					{uploadedFiles && (
						<div className="border text-center border-opacity-50 border-solid border-dimwhite w-[95%] mx-auto my-[2px]"></div>
					)}
					<div className="flex items-center w-full py-2">
						<textarea
							value={text}
							onChange={(e) => setText(e.target.value)}
							onInput={(e) => {
								const target = e.target as HTMLTextAreaElement
								target.style.height = "auto"
								target.style.height = target.scrollHeight + "px"
							}}
							rows={1}
							className="my-0 py-0 w-full px-14 font-montserrat font-medium text-[16px] leading-[19.5px] resize-none outline-none overflow-y-auto max-h-[150px] text-primary-200"
							placeholder="Type here..."
						/>
					</div>
					<div
						onClick={sendMessage}
						className="absolute bottom-[6px] right-3 text-white flex items-center  p-2 rounded-full bg-primary-300 cursor-pointer">
						<SendHorizonal className="bg-transparent " />
					</div>
					<div className="absolute bottom-[-3px] left-4 transform -translate-y-1/2 bg-inherit text-primary-300 flex items-center  cursor-pointer">
						<input
							type="file"
							ref={fileInputRef}
							style={{ display: "none" }}
							onChange={handleUploadFileChange}
							accept="image/*"
						/>
						<button
							className="cursor-pointer bg-inherit flex item-center"
							onClick={handleUploadClick}>
							<ImageUp className="bg-transparent h-[30px] w-[30px] text-primary-300" />
						</button>
					</div>
				</div>
				<span className="max-w-[464.93px] w-full h-[15.71px] font-montserrat font-[400] text-[12px] leading-[14.63px] text-primary-300 text-center">
					KleeneStar can make mistakes. Consider checking important information.
				</span>
			</div>
			<div className="absolute bottom-[12.45px] right-[12.54px] bg-inherit text-primary-300 mq850:hidden ">
				<CircleHelp className="bg-transparent" />
			</div>
			{/* <section className="rounded-3xl  w-full h-full p-4 md:px-[91.97px] md:py-[21.35px] flex flex-col relative gap-[29.94px] scrollbar bg-white">
                <div className=" w-full h-full flex flex-col overflow-auto ">
                    <div className="flex-1 ">
                        <NewChatDisplay />
                    </div>
                </div>
            </section> */}
		</div>
	)
}

export default ChatDisplay
