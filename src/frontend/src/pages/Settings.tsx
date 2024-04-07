import ChangePasswordSection from "../components/ChangePasswordSection"
import ProfileSection from "../components/ProfileSection"
import SlideSwitch from "../components/SlideSwitch"
import { ChevronDown, CircleArrowLeft } from "lucide-react"
import { FolderClosed } from "lucide-react"
import { useNavigate } from "react-router-dom"
import SelectOptions from "../components/SelectOptions"

function Settings(): JSX.Element {
	const reasonsToDeleteAccount = [
		"Found a better platform/service",
		"Concerns about privacy/security",
		"No longer need the account/service",
		"Dissatisfaction with the platform/service",
		"Simplifying digital footprint",
	]

  const navigate = useNavigate()
  return (
		<div className="w-screen bg-background pb-20">
			<div className="pt-10 pl-8 mq750:pl-0 ">
				<div className="text-primary-300 mq750:px-10 flex gap-8 mq750:justify-between items-center">
					<CircleArrowLeft
						className="w-[30px] h-[30px]  "
						onClick={() => navigate(-1)}
					/>
					<div className="text-primary-300 font-syne text-[1.6rem] font-bold mq750:text-[20px]">
						Settings
					</div>
					<div className="hidden mq750:block">
						<FolderClosed size={30} />
					</div>
				</div>
				<div className="font-montserrat text-primary-300 flex px-[5rem] mq750:w-full mq750:px-[2.2rem] mq750:text-center justify-between">
					<p className="whitespace-nowrap mq750:mx-auto">
						Manage your profile details.
					</p>
					<p className="mq750:hidden">
						<u>Archived chats</u>
					</p>
				</div>
			</div>
			<div className="w-[90%] gap-[5%] relative top-10 mx-auto mq750:flex-col flex">
				<ProfileSection />
				<div className="w-[50%] mq750:w-[95%] mq750:mx-auto mq750:mt-10 flex-col ">
					<ChangePasswordSection />
					<div className="bg-white rounded-[2rem] h-fit  mt-4 ">
						<div className="text-primary-300 font-montserrat pt-2 pl-8 pb-4 my-4 ">
							<div className=" font-bold pr-10 mq750:pr-4 mq750:text-[16px]  text-[1.6rem] flex justify-between my-4">
								Google Authenticator
								<SlideSwitch on={true} />
							</div>
							<p className="mq750:text-[14px] mq750:pr-2">
								Use the Google Authenticator app to generate one time security
								codes.
							</p>
						</div>
					</div>
					<div className="bg-white rounded-[2rem] h-fit mt-4 ">
						<div className="text-primary-300 font-montserrat pt-2 pl-8 pb-4">
							<div className=" font-bold mq750:text-[16px] pr-10 mq750:pr-4 text-[1.6rem] flex justify-between my-4">
								Two Factor Authentication
								<SlideSwitch on={true} />
							</div>
							<p className="mq750:text-[14px] mq750:pr-2">
								Require a second authentication method in addition to your
								password.
							</p>
						</div>
					</div>
				</div>
			</div>
			<div className="w-[90%] mq750:w-[85%] mx-auto mt-20 bg-white rounded-[2rem]">
				<div className="text-primary-300 font-montserrat pt-2 pl-8 pb-4 mq750:pl-4  mq750:pr-2 ">
					<p className=" font-bold text-[1.6rem] mq750:text-[16px]">
						Delete Account
					</p>
					<p className="mq750:text-[14px]">
						Deleting your account will close your workspace, stop all activities
						from our service, and purge all your information from our database.
						This cannot be undone. 😱
					</p>
					<div className="flex justify-between items-center pr-4 pb-4 mq750:flex-col">
						<div className="w-[60%]  mq750:w-full text-primary-300 font-bold text-xl">
							<div className=" mt-2 mq750:h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
								<SelectOptions
									options={reasonsToDeleteAccount}
									InputText={"To confirm, tell us why you are leaving."}
								/>
								<ChevronDown className="text-primary-300" />
							</div>
						</div>
						<div className="border-2 items-center flex whitespace-nowrap mq750:text-[15px] mq750:mt-4 mq750:py-[0.5rem] mq750:px-16 hover:text-white hover:bg-red-500 cursor-pointer w-fit px-10 rounded-[2rem] py-[1rem] border-solid border-red-500 text-red-500">
							Delete Account
						</div>
					</div>
				</div>
			</div>
		</div>
	)
}

export default Settings
