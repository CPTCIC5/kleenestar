import {CircleX, Ellipsis, Folders, FolderUp, PenLine, SquarePen, Trash2, Menu } from "lucide-react"
import {
	dummyChatListToday,
	dummyChatListPrevious,
} from "../utils/dummyChatList.js"
import {useEffect, useState, useRef} from 'react'

function ChatSideBar() {
	const [currentConvo, setCurrentConvo] = useState("")
	const [renameActive, setRenameActive] = useState("")
	const list = useRef<HTMLDivElement>(null)
	useEffect(() => {
		if (renameActive) {
			if (list.current) {
				list.current.style.overflow = "hidden";
			}
		}else{
			if (list.current) {
				list.current.style.overflow = "auto"
			}
		}
	}, [renameActive]);
	const SideBar = useRef<HTMLDivElement>(null)

	const handleHide = () => {
		if (SideBar.current) {
			if (SideBar.current.style.transform === "translateX(-100%)") {
				SideBar.current.style.transform = "translateX(0)"
			} else {
				SideBar.current.style.transform = "translateX(-100%)"
			}
		}
	}
	return (
		<div className="h-screen w-full bg-background flex justify-between">
			<aside ref={SideBar}  className="bg-inherit transform transition-all duration-300 mq750:rounded-r-3xl mq750:rounded-b-3xl  mq750:max-w-[324px]  max-w-[375.93px] w-full h-full flex flex-col ">
				<div className="bg-primary-300 mq750:max-w-[324px] max-w-[375.93px]  mq750:rounded-se-2xl  z-10 absolute h-[86.91px] mq750:h-[81px] w-full flex items-center justify-evenly  px-[26.54px] py-[16.06px]">
					<div className="flex items-center justify-center gap-[18.13px]">
						<div className="mq750:block hidden mq750:pr-[31.67px]">
							<CircleX
								className="w-[30px] mt-1 text-white min-w-[20px] h-[30px] mq750:w-[20px] mq750:h-[20px]  "
								onClick={handleHide}
							/>
						</div>
						<div className="w-fit mq750:hidden">
							<img
								className="w-[52.07px] h-[54.78px]"
								src="/group_72.png"
								alt=""
							/>
						</div>

						<span className="w-[156.02px] mq750:text-[20px] font-syne text-white font-[700] text-[25px] leading-[30px]">
							Kleenestar
						</span>
					</div>
					<SquarePen className="w-[20.94px] text-white h-[20.94px] cursor-pointer" />
				</div>
				<div className=" bg-white   text-primary-300 font-montserrat  h-[100vh]  mq750:rounded-se-2xl w-full">
					<div ref={list} className="pt-[86.91px]   hide-scrollbar  pb-[124.6px] max-h-[100vh] mq750:max-h-[95vh] mq750:mt-[20px] overflow-auto  w-full mq750:pt-[61px]">
						<div className="px-[25.77px] mq750:px-[27.17px] mq750:py-[23px]  w-full py-[25.13px]">
							<p className="text-[12px] font-[400] pb-[13.61px]">Today</p>
							<div className="text-[15px]">
								{dummyChatListToday.map((name: string, index: number) => {
									if (name === currentConvo) {
										return (
											<div
												onClick={() => {
													setCurrentConvo(name)
												}}
												key={index}
												className="w-full  pl-[19.05px] justify-between flex pr-[17.75px] pt-[10.83px] rounded-3xl h-[47.12px] text-white bg-primary-300">
												<div className="w-fit max-w-[205.24px] overflow-hidden whitespace-nowrap text-ellipsis">
													{name}
												</div>
												<Ellipsis
													onClick={() => {
														name === renameActive
															? setRenameActive("")
															: setRenameActive(name)
													}}
													className="mq750:hidden cursor-pointer"
												/>
												{renameActive === name && (
													<div className="w-[188.75px] drop-shadow-2xl whitespace-nowrap h-[189px] flex-col  rounded-2xl left-[350px] text-primary-300 font-[500]  bg-white absolute z-1 ">
														<div className="px-[30.26px] pt-[15px]">
															<div className="py-2 flex gap-[17.41px] items-center">
																<PenLine />
																Rename
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<FolderUp />
																Share Chat
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<Folders />
																Archive
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<Trash2 />
																Delete Chat
															</div>
														</div>
													</div>
												)}
											</div>
										)
									} else {
										return (
											<div
												onClick={() => {
													setCurrentConvo(name)
												}}
												key={index}
												className="w-full group hover:bg-gray-100 hover:text-primary-300  hover:transform hover:transition-all hover:duration-200  justify-between flex pr-[17.75px] pl-[19.05px] pt-[10.83px] rounded-3xl h-[47.12px] bg-white">
												<div className="w-fit max-w-[205.24px] overflow-hidden whitespace-nowrap text-ellipsis">
													{name}
												</div>

												<Ellipsis
													onClick={() => {
														name === renameActive
															? setRenameActive("")
															: setRenameActive(name)
													}}
													className="mq750:hidden cursor-pointer group-hover:block hidden"
												/>
												{renameActive === name && (
													<div className="w-[188.75px] drop-shadow-2xl whitespace-nowrap h-[189px] flex-col  rounded-2xl left-[350px] text-primary-300 font-[500]  bg-white absolute z-1 ">
														<div className="px-[30.26px] pt-[15px]">
															<div className="py-2 flex gap-[17.41px] items-center">
																<PenLine />
																Rename
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<FolderUp />
																Share Chat
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<Folders />
																Archive
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<Trash2 />
																Delete Chat
															</div>
														</div>
													</div>
												)}
											</div>
										)
									}
								})}
							</div>
							<p className="text-[12px] pt-[23.04px] font-[400] pb-[13.61px]">
								Previous 7 days
							</p>
							<div className="text-[15px]">
								{dummyChatListPrevious.map((name: string, index: number) => {
									if (name === currentConvo) {
										return (
											<div
												onClick={() => {
													setCurrentConvo(name)
												}}
												key={index}
												className="w-full  justify-between flex pr-[17.75px] pl-[19.05px] pt-[10.83px] rounded-3xl h-[47.12px] text-white bg-primary-300">
												<div className="w-fit max-w-[205.24px] overflow-hidden whitespace-nowrap text-ellipsis">
													{name}
												</div>
												<Ellipsis
													onClick={() => {
														name === renameActive
															? setRenameActive("")
															: setRenameActive(name)
													}}
													className=" mq750:hidden cursor-pointer"
												/>
												{renameActive === name && (
													<div className="w-[188.75px] drop-shadow-2xl whitespace-nowrap h-[189px] flex-col  rounded-2xl left-[350px] text-primary-300 font-[500]  bg-white absolute z-1 ">
														<div className="px-[30.26px] pt-[15px]">
															<div className="py-2 flex gap-[17.41px] items-center">
																<PenLine />
																Rename
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<FolderUp />
																Share Chat
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<Folders />
																Archive
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<Trash2 />
																Delete Chat
															</div>
														</div>
													</div>
												)}
											</div>
										)
									} else {
										return (
											<div
												onClick={() => {
													setCurrentConvo(name)
												}}
												key={index}
												className="w-full group hover:bg-gray-100 hover:text-primary-300  hover:transform hover:transition-all hover:duration-200 justify-between flex pr-[17.75px] pl-[19.05px] pt-[10.83px] rounded-3xl h-[47.12px] bg-white">
												<div className="w-fit max-w-[205.24px] overflow-hidden whitespace-nowrap text-ellipsis">
													{name}
												</div>
												<Ellipsis
													onClick={() => {
														name === renameActive
															? setRenameActive("")
															: setRenameActive(name)
													}}
													className="mq750:hidden group-hover:block hidden cursor-pointer"
												/>
												{renameActive === name && (
													<div className="w-[188.75px] drop-shadow-2xl whitespace-nowrap h-[189px] flex-col  rounded-2xl left-[350px] text-primary-300 font-[500]  bg-white absolute z-1 ">
														<div className="px-[30.26px] pt-[15px]">
															<div className="py-2 flex gap-[17.41px] items-center">
																<PenLine />
																Rename
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<FolderUp />
																Share Chat
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<Folders />
																Archive
															</div>
															<div className="py-2 flex gap-[17.41px] items-center">
																<Trash2 />
																Delete Chat
															</div>
														</div>
													</div>
												)}
											</div>
										)
									}
								})}
							</div>
						</div>
					</div>
				</div>

				<div className="z-10 font-montserrat mq750:max-w-[324px] bg-white absolute bottom-0 mq750:rounded-b-2xl w-full max-w-[375.93px]  top-100 h-[124.6px]">
					<div className="px-[25.77px] py-[15.18px]">
						<div className="w-full font-[500] text-[15px] hover:bg-gray-100 hover:text-primary-300  hover:transform hover:transition-all hover:duration-200 justify-start gap-[25.37px] flex pr-[17.75px] pl-[19.05px] pt-[10.83px] rounded-3xl h-[47.12px] bg-white">
							<img
								src="/profile-chat.png"
								alt=""
								className="w-[28px] h-[28px]"
							/>
							Add team to workspace
						</div>
						<div className="w-full items-center  justify-between flex pr-[17.75px] pl-[19.05px] pt-[10.83px] rounded-3xl h-[47.12px] bg-white">
							<div className="flex font-[500] text-[15px] gap-[17.58px] items-center">
								<div className=" bg-gradient-to-b from-amber-100 to-peach-200  rounded-full w-[38.45px] h-[38.45px]  border-solid border-primary-300 border-2 "></div>
								Craig Donovan
							</div>

							<Ellipsis />
						</div>
					</div>
				</div>
			</aside>
			<div className="w-fit p-4 h-20 bg-white">
				<Menu className="h-10" onClick={handleHide} />
			</div>
			

		</div>
	)
}

export default ChatSideBar
