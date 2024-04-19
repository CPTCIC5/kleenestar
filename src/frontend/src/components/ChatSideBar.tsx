import { CircleX, Ellipsis, Folders, FolderUp, LogOut, PenLine, Settings, ShoppingBag, SquarePen, Trash2, UsersRound, Zap } from "lucide-react";
import { dummyChatListToday, dummyChatListPrevious } from "../utils/dummyChatList.js";
import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
interface ChatSideBarProps {
    SideBar: React.RefObject<HTMLDivElement>;
    handleHide: () => void;
}

const ChatSideBar: React.FC<ChatSideBarProps> = ({ SideBar, handleHide }) => {
    const [currentConvo, setCurrentConvo] = useState("");
    const [renameActive, setRenameActive] = useState("");
    const list = useRef<HTMLDivElement>(null);
	const profile = useRef<HTMLDivElement>(null);
    useEffect(() => {
        if (renameActive) {
            if (list.current) {
                list.current.style.overflow = "hidden";
            }
        } else {
            if (list.current) {
                list.current.style.overflow = "auto";
            }
        }
    }, [renameActive]);
	useEffect(() => {
		const handleClick = () => {
			if(renameActive){
				setRenameActive("")
			}
			if(profile.current){
				if (profile.current.style.display === "block") {
					profile.current.style.display = "none"
				} 
			}
		}
		document.body.addEventListener("click", handleClick)

		return () => {
			document.body.removeEventListener("click", handleClick)
		}
	}, [renameActive])
	const navigate = useNavigate()

	const handleProfile = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
		e.stopPropagation()
		if (profile.current) {
			if (profile.current.style.display === "block") {
				profile.current.style.display = "none"
			} else {
				profile.current.style.display = "block"
			}
		}
	}
    return (
			<aside
				ref={SideBar}
				className="bg-inheritmq750 mq750:absolute z-30 transform transition-all duration-300 mq750:rounded-r-3xl mq750:rounded-b-3xl  mq750:max-w-[324px]  max-w-[375.93px] w-full h-full flex flex-col ">
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
				<div className=" bg-background   text-primary-300 font-montserrat  h-[100vh]  mq750:rounded-se-2xl w-full">
					<div
						ref={list}
						className="pt-[86.91px]   hide-scrollbar  pb-[124.6px] max-h-[100vh] mq750:max-h-[95vh] mq750:mt-[20px] overflow-auto  w-full mq750:pt-[61px]">
						<div className=" bg-background px-[25.77px] mq750:px-[27.17px] mq750:py-[23px]  w-full py-[25.13px]">
							<p className="text-[12px] font-[400] pb-[13.61px]">Today</p>
							<div className="text-[15px]">
								{dummyChatListToday.map((name: string, index: number) => {
									if (name === currentConvo) {
										return (
											<div
												onClick={(e) => {e.stopPropagation()
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
													<div className="w-[188.75px] drop-shadow-2xl whitespace-nowrap h-[189px] flex-col  rounded-2xl left-[350px] text-primary-300 font-[500]  bg-background absolute z-20 ">
														<div className="px-[30.26px] pt-[15px]">
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<PenLine />
																Rename
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<FolderUp />
																Share Chat
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<Folders />
																Archive
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
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
												onClick={(e) => {	e.stopPropagation()
													setCurrentConvo(name)
												}}
												key={index}
												className="w-full group hover:bg-gray-100 hover:text-primary-300  hover:transform hover:transition-all hover:duration-200  justify-between flex pr-[17.75px] pl-[19.05px] pt-[10.83px] rounded-3xl h-[47.12px] bg-background">
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
													<div className="w-[188.75px] drop-shadow-2xl whitespace-nowrap h-[189px] flex-col  rounded-2xl left-[350px] text-primary-300 font-[500]  bg-background absolute z-20 ">
														<div className="px-[30.26px] pt-[15px]">
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<PenLine />
																Rename
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<FolderUp />
																Share Chat
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<Folders />
																Archive
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
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
												onClick={(e) => {	e.stopPropagation()
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
													<div className="w-[188.75px] drop-shadow-2xl whitespace-nowrap h-[189px] flex-col  rounded-2xl left-[350px] text-primary-300 font-[500]  bg-background absolute z-20 ">
														<div className="px-[30.26px] pt-[15px]">
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<PenLine />
																Rename
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<FolderUp />
																Share Chat
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<Folders />
																Archive
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
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
												onClick={(e) => {e.stopPropagation()
													setCurrentConvo(name)
												}}
												key={index}
												className="w-full group hover:bg-gray-100 hover:text-primary-300  hover:transform hover:transition-all hover:duration-200 justify-between flex pr-[17.75px] pl-[19.05px] pt-[10.83px] rounded-3xl h-[47.12px] bg-background">
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
													<div className="w-[188.75px] drop-shadow-2xl  whitespace-nowrap h-[189px] flex-col  rounded-2xl left-[350px] text-primary-300 font-[500]  bg-background absolute z-20 ">
														<div className="px-[30.26px] pt-[15px]">
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<PenLine />
																Rename
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<FolderUp />
																Share Chat
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
																<Folders />
																Archive
															</div>
															<div className="py-2 flex gap-[17.41px] items-center cursor-pointer">
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
				<div className="z-10 font-montserrat mq750:max-w-[324px] bg-background absolute bottom-0 mq750:rounded-b-2xl w-full max-w-[375.93px]  top-100 h-[124.6px]">
					<div className="border text-center border-opacity-50 border-solid border-dimwhite w-[95%] mx-auto my-[2px]"></div>

					<div className="px-[25.77px] py-[15.18px]">
						<div className="w-full font-[500] text-[15px] hover:bg-gray-100 hover:text-primary-300  hover:transform hover:transition-all hover:duration-200 justify-start gap-[25.37px] flex pr-[17.75px] pl-[19.05px] pt-[10.83px] rounded-3xl h-[47.12px] bg-background">
							<img
								src="/profile-chat.png"
								alt=""
								className="w-[28px] h-[28px]"
							/>
							Add team to workspace
						</div>
						<div ref={profile}  className="w-full bg-white bottom-[60px] left-[30px] absolute h-[301px] max-w-[310px] mq750:max-w-[269.73px] rounded-3xl drop-shadow-2xl z-30">
							<div className="w-fit ml-[30.02px] font-[500] font-montserrat text-primary-300 text-[15px] py-[23px]">
								<div
									onClick={() => {
										navigate("/billings")
									}}
									className="flex items-center justify-between gap-[16.3px] cursor-pointer ">
									<ShoppingBag />
									My Plans
									<div className="font-syne ml-[73px] mq750:ml-[33px]   rounded-xl px-[10px] py-[5px] font-[700] text-[13px] text-white bg-royalblue  ">
										Scale
									</div>
								</div>
								<div
									onClick={() => {
										navigate("/channels")
									}}
									className="flex gap-[16.3px] cursor-pointer pt-[32px]">
									<Zap className="absolute left-[35px] w-[18px]  " />
									<div className="w-[25px] h-[25px] rounded-full border-primary-300 border-solid border-[2.2px]"></div>
									My Channels
								</div>
								<div
									onClick={() => {
										navigate("/settings")
									}}
									className="flex gap-[16.3px] cursor-pointer pt-[32px]">
									<Settings />
									Settings
								</div>
								<div
									onClick={() => {
										navigate("")
									}}
									className="flex gap-[16.3px] cursor-pointer pb-[10px] pt-[32px]">
									<UsersRound />
									Help center
								</div>
								<div className="border absolute right-2 text-center border-opacity-50 border-solid border-dimwhite w-[95%] mx-auto my-[2px]"></div>

								<div
									className="flex gap-[16.3px] cursor-pointer pt-[20px] ">
									<LogOut />
									Log out
								</div>
							</div>
						</div>
						<div
							onClick={handleProfile}
							className="w-full cursor-pointer hover:bg-gray-100 hover:text-primary-300  hover:transform hover:transition-all hover:duration-200 items-center  justify-between flex pr-[17.75px] pl-[19.05px] py-[10.83px] rounded-3xl h-[47.12px] bg-background">
							<div className="flex font-[500] text-[15px] gap-[17.58px] items-center">
								<div className=" bg-gradient-to-b from-amber-100 to-peach-200  rounded-full w-[38.45px] h-[38.45px]  border-solid border-primary-300 border-2 "></div>
								Craig Donovan
							</div>

							<Ellipsis />
						</div>
					</div>
				</div>
			</aside>
		)
};

export default ChatSideBar;
