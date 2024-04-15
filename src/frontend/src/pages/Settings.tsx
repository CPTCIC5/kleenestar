import ChangePasswordSection from "../components/ChangePasswordSection"
import ProfileSection from "../components/ProfileSection"
import SlideSwitch from "../components/SlideSwitch"
import { ChevronDown, CircleArrowLeft } from "lucide-react"
import { FolderClosed } from "lucide-react"
import { useNavigate } from "react-router-dom"
import SelectOptions from "../components/SelectOptions"

function Settings(): JSX.Element {
	const reasonsToDeleteAccount = [
		{
			name: "Found a better platform/service",
			value: "Found a better platform/service",
		},
		{
			name: "No longer need the account/service",
			value: "No longer need the account/service",
		},
		{
			name: "Dissatisfaction with the platform/service",
			value: "Dissatisfaction with the platform/service",
		},
		{
			name: "Simplifying digital footprint",
			value: "Simplifying digital footprint",
		},
	]

	const navigate = useNavigate()
	return (
		<div className=" h-ful w-screen min-h-screen bg-background pb-20">
			<div className="w-full pl-8 mq1000:pl-0 ">
				<div className="text-primary-300 mq1000:fixed z-30 w-full mq1000:bg-white py-[20px]  mq1000:px-10 flex gap-8 mq1000:justify-between items-center">
					<CircleArrowLeft
						className="w-[30px] min-w-[20px] h-[30px] mq1000:w-[20px] mq1000:h-[20px]  "
						onClick={() => navigate(-1)}
					/>
					<div className="text-primary-300 font-syne text-[1.6rem] font-bold mq1000:text-[20px]">
						Settings
					</div>
					<div className="hidden mq1000:block">
						<FolderClosed className="w-[30px] min-w-[20px] h-[30px] mq1000:w-[20px] mq1000:h-[20px]" />
					</div>
				</div>
				<div className="font-montserrat mq1000:top-[100.5px] mq1000:relative text-primary-300 flex px-[5rem] mq1000:w-full mq1000:px-[10vw] mq1000:text-center justify-between">
					<p className="whitespace-nowrap text-center mq1000:mx-auto">
						Manage your profile details.
					</p>
					<p className="mq1000:hidden">
						<u>Archived chats</u>
					</p>
				</div>
			</div>
			<div className="w-[90%] gap-[5%] relative top-10 mq1000:top-[139px] mx-auto mq1000:flex-col flex">
				<ProfileSection />
				<div className="w-[50%] mq1000:w-[95%] mq1000:mx-auto mq1000:mt-10 flex-col ">
					<ChangePasswordSection />
					<div className="bg-white rounded-[2rem] h-fit  mt-4 ">
						<div className="text-primary-300 font-montserrat pt-2 pl-8 pb-4 my-4 ">
							<div className=" font-bold pr-10 mq1000:pr-4 text-[16px]   flex justify-between my-4">
								Google Authenticator
								<SlideSwitch on={true} />
							</div>
							<p className="text-[14px] mq1000:pr-2">
								Use the Google Authenticator app to generate one time security
								codes.
							</p>
						</div>
					</div>
					<div className="bg-white rounded-[2rem] h-fit mt-4 ">
						<div className="text-primary-300 font-montserrat pt-2 pl-8 pb-4">
							<div className=" font-bold text-[16px] pr-10 mq1000:pr-4  flex justify-between my-4">
								Two Factor Authentication
								<SlideSwitch on={true} />
							</div>
							<p className="text-[14px] mq1000:pr-2">
								Require a second authentication method in addition to your
								password.
							</p>
						</div>
					</div>
				</div>
			</div>
			<div className="w-[90%] mq1000:w-[85%] mx-auto mt-20 mq1000:mt-40 bg-white rounded-[2rem]">
				<div className="text-primary-300 pt-[28px]  font-montserrat px-8 pb-4 mq1000:pl-4  mq1000:pr-2 ">
					<p className=" font-bold text-[16px]">Delete Account</p>
					<p className="text-[14px] pt-2">
						Deleting your account will close your workspace, stop all activities
						from our service, and purge all your information from our database.
						This cannot be undone. 😱
					</p>
					<div className="flex justify-between items-center pr-4 py-4 mq1000:flex-col">
						<div className="w-[60%]  mq1000:w-full text-primary-300 font-bold text-xl">
							<div className=" mt-2   bg-background rounded-[2rem] px-[26.57px] flex items-center ">
								<SelectOptions
									options={reasonsToDeleteAccount}
									InputText={"To confirm, tell us why you are leaving."}
								/>
								<ChevronDown className="text-primary-300" />
							</div>
						</div>
						<div className="border-2 items-center flex whitespace-nowrap text-[15px] mq1000:mt-4 mq1000:py-[0.5rem] mq1000:px-14 hover:text-white hover:bg-red-500 cursor-pointer w-fit px-10 rounded-[2rem] py-[10px] border-solid border-red-500 text-red-500">
							Delete Account
						</div>
					</div>
				</div>
			</div>
		</div>
	)
}

export default Settings
