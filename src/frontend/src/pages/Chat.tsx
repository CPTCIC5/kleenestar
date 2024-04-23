// import React, { useEffect, useState } from "react";
import { FunctionComponent, useEffect, useRef, useState } from "react"
// import { CircleHelp, ImageUp, SendHorizonal, SquarePen } from "lucide-react";
// import NewChatDisplay from "../components/NewChatDisplay";
import ChatSideBar from "../components/ChatSideBar"
import ChatDisplay from "../components/ChatDisplay"
// import axios from "axios";
import InviteTeam from "../modals/InviteTeam"
import { useNavigate } from "react-router-dom"
import axios from 'axios'
import Cookies from 'js-cookie'

const Chat: FunctionComponent = () => {
    const navigate = useNavigate()
	const [isLoggedIn, setIsLoggedIn] = useState(false)
	const [userDetails, setUserDetails] = useState<{
		id: string
		profile: { country: string }
	}>({
		id: "",
		profile: {
			country: "",
		},
	})
	useEffect(() => {
		const fetchWorkspaceDetails = async () => {
			try {
				const response = await axios.get(
					"http://127.0.0.1:8000/api/workspaces/",
					{
						withCredentials: true,
						headers: {
							"Content-Type": "application/json",
							"X-CSRFToken": Cookies.get("csrftoken"),
						},
					}
				)
				setIsLoggedIn(true)
				setUserDetails(response.data[0].root_user)
			} catch (err) {
                console.error(err)
				navigate("/")
			}
		}
		fetchWorkspaceDetails()
	}, [navigate])
    
	const SideBar = useRef<HTMLDivElement>(null)
	const [inviteOpen, setInviteOpen] = useState(false)
	const handleHide = () => {
		if (SideBar.current) {
			if (SideBar.current.style.transform === "translateX(-100%)") {
				setTimeout(() => {
					if (SideBar.current) {
						SideBar.current.style.transform = "translateX(0)"
					}
				}, 20) // Adjust this delay to match your transition duration

				SideBar.current.style.display = "block"
			} else {
				SideBar.current.style.transform = "translateX(-100%)"

				setTimeout(() => {
					if (SideBar.current) {
						SideBar.current.style.display = "none"
					}
				}, 75) // Adjust this delay to match your transition duration
			}
		}
	}
    if(!isLoggedIn){
        return <></>
    }
	return (
		<div className="h-screen flex overflow-hidden">
			<ChatSideBar
				SideBar={SideBar}
				handleHide={handleHide}
				setInviteOpen={setInviteOpen}
			/>
			<ChatDisplay handleHide={handleHide} />
			<InviteTeam
				isOpen={inviteOpen}
				onClose={setInviteOpen}
			/>
		</div>
	)
}

export default Chat
