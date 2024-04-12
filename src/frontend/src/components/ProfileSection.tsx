import { PencilLine } from "lucide-react"
import { ChevronDown } from "lucide-react"
import {useRef} from 'react'
import SelectOptions from "./SelectOptions";
import {countries} from '../utils/countries.json'

function ProfileSection(): JSX.Element {

	const imageRef = useRef<HTMLInputElement>(null);
	const handleAvatarClick = () => {
		if (imageRef.current) {
			imageRef.current.click();
		}
	};
	return (
		<div className="w-[50%] bg-white mq1000:w-[95%] mq1000:mx-auto rounded-[2rem] ">
			<div className="text-primary-300  font-montserrat pt-[28px] pl-8 pb-4 mq1000:pl-4 border-solid border-b-2 border-[#BEB9B1] ">
				<p className=" font-bold text-[16px]"> Profile</p>
				<p className="text-[14px] whitespace-nowrap">
					Mange your profile details
				</p>
			</div>
			<div className="py-4 flex items-center gap-4 pl-8 ">
				<div className="w-fit bg-gradient-to-b from-amber-100 to-peach-200 h-fit rounded-full py-[3.5rem] px-[3.6rem] mq1000:px-[2.2rem] mq1000:py-[2.2rem] border-solid border-primary-300 border-4 "></div>
				<div>
					<input
						ref={imageRef}
						className="hidden"
						type="file"
						name="files"
						id=""
					/>
					<img
						onClick={handleAvatarClick}
						src="/add_image.png"
						className="w-[30px] mq1000:w-6"
						alt=""
					/>
				</div>
			</div>
			<div className="p-2 pt-4  w-full font-montserrat text-lg ">
				<div className="w-[95%] mx-auto">
					<div className="flex items-center justify-center mq1000:flex-col gap-4">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							First name
							<div className="w-full mt-2 bg-background rounded-[2rem] p-4 flex items-center h-[45px] ">
								<input
									type="text"
									placeholder="First name"
									className="font-montserrat autofill:bg-transparent outline-none bg-transparent w-full text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Last name
							<div className="w-full mt-2 bg-background h-[45px] rounded-[2rem] p-4 flex items-center ">
								<input
									type="text"
									placeholder="Last name"
									className="autofill:bg-transparent outline-none bg-transparent w-full font-montserrat  text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
					</div>
					<div className="flex items-center justify-center gap-4 pt-2 mq1000:flex-col">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Email address
							<div className="w-full h-[45px] mt-2 bg-[#D1D3DB] rounded-[2rem] p-4 flex items-center ">
								<input
									pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
									type="text"
									placeholder="Email address"
									className="autofill:bg-transparent outline-none bg-transparent font-montserrat w-full text-[15px]"
								/>
								<PencilLine className="text-primary-300 bg-transparent" />
							</div>
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Workspace name
							<div className="w-full mt-2 h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									type="text"
									placeholder="Workspace name"
									className="autofill:bg-transparent outline-none bg-transparent w-full font-montserrat text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
					</div>
					<div className="flex items-center justify-center gap-4 pt-2 mq1000:flex-col">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Country
							<div className="w-full px-[19.34px]  mt-2 bg-background  rounded-[2rem]  flex items-center ">
								<SelectOptions
									options={countries}
									InputText={"Country"}
								/>
								<ChevronDown className="text-primary-300 w-fit" />
							</div>
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Phone number
							<div className="w-full h-[45px] mt-2 bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									type="text"
									placeholder="Phone number"
									className="autofill:bg-transparent outline-none bg-transparent w-full font-montserrat text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
					</div>
					<div className="w-full font-bold rounded-[2rem] my-8 cursor-pointer text-white text-[15px]  mq1000:py-[0.7rem] bg-primary-300 text-center py-[10px]">
						Save changes
					</div>
				</div>
			</div>
		</div>
	)
}

export default ProfileSection
