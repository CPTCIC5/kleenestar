import { CircleX, Ellipsis, LinkIcon, PencilLine } from "lucide-react";
import React from "react";
import PrimaryButton from "../components/PrimaryButton";
import { Link } from "react-router-dom";
import dummyInviteTeam from "../utils/dummyInviteTeam.json";
import {z} from 'zod'
import { SubmitHandler, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
interface InviteTeamProps {
    // define your props here
    isOpen: boolean;
    onClose: (option: boolean) => void;
}
const schema = z.object({
    email: z.string().email({message: "Invalid Email Address"})
})

type FormFields = z.infer<typeof schema>
const InviteTeam: React.FC<InviteTeamProps> = ({ isOpen, onClose }) => {
    const sendEmailInvite: SubmitHandler<FormFields> = (data) =>{
        console.log(data)
    } 
    const {register, handleSubmit, formState} = useForm({
        defaultValues: {
            email: ""
        },
        resolver: zodResolver(schema),
        mode: "onChange"
    })
    const {isValid, errors} = formState
    return (
			<>
				{isOpen ? (
					<div
						className="fixed inset-0 z-50 bg-black bg-opacity-30 flex items-center p-0 justify-end"
						onClick={() => onClose(isOpen)}>
						<div
							className=" max-w-[551px] w-full h-full bg-whitesmoke rounded-l-3xl flex flex-col items-start rounded-tl-3xl overflow-auto mq551:rounded-l-none "
							onClick={(e) => e.stopPropagation()}>
							<CircleX
								onClick={() => onClose(isOpen)}
								className="absolute z-10 top-[25px] right-[32px] h-[38px] w-[38px] text-primary-300 bg-transparent mq551:h-[28px] mq551:w-[28px] mq551:top-[10px] mq551:right-[10px]"
								strokeWidth={1}
							/>
							<div className="w-full pt-[42.5px] pl-[80px] pb-[19px] flex gap-[19px] mq551:fixed mq551:bg-white mq551:flex mq551:items-center mq551:justify-center mq551:pl-0 ">
								<span className="font-syne font-[700] text-[30px] leading-[36px] text-primary-300 mq374:text-[25px] ">
									Invite team
								</span>
							</div>

							<div className="w-full pl-[80px] flex flex-col mq551:mt-[120px] mq551:pl-0 mq551:flex mq551:flex-col mq551:items-center gap-[18px] ">
								<div className="max-w-[387px] w-full font-montserrat font-[400] text-[16px] leading-[19.5px] text-primary-300 text-start mq551:text-center mq551:px-4">
									Send email invites to members.
								</div>
								<div className="w-full h-full flex flex-col mq551:px-4 mq551:items-center  ">
									<div className="max-w-[388.62px] w-full flex flex-col items-center">
										<div className="relative w-full h-[45px] flex items-center">
											<input
												{...register("email", {
													required: "Email Is Required",
												})}
												type="email"
												name="email"
												placeholder="@work-email.com"
												className="bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300 outline-none focus:outline-primary-100 focus:outline"
											/>
											{/* PrimaryInputBox component for email*/}
											<div className="absolute bg-inherit text-primary flex items-center right-4">
												<PencilLine className="bg-inherit " />
											</div>
										</div>
										{errors.email && (
											<div className="w-full pt-[20px] pl-[10px] h-[16px] flex items-center justify-start">
												<span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
													{errors.email.message}
												</span>
											</div>
										)}
										<div className="h-[40px] max-w-[267.37px] w-full mt-[30px]">
											<PrimaryButton
												disabled={!isValid}
												onClick={handleSubmit(sendEmailInvite)}>
												Send Invite
											</PrimaryButton>
											{/* Use the PrimaryButton component */}
										</div>

										<div className="flex items-center justify-center gap-[12px] mt-[19px]">
											<LinkIcon className="text-primary-300 h-[20px] w-[20px]" />
											<span className="font-montserrat font-[400] text-[14px] leading-[18px] text-primary-300">
												<Link
													to={"#"}
													className="underline text-inherit ">
													Get a shareable invite link
												</Link>{" "}
												instead
											</span>
										</div>
									</div>
								</div>
							</div>
							<div className="border border-opacity-50 border-solid border-dimwhite w-full mt-[37.5px]"></div>
							<div className="w-full pl-[80px] pt-[29px] mq551:px-0 mq551:flex mq551:flex-col mq551:items-center overflow-auto mb-[40px]">
								<div className="max-w-[388.62px] w-full flex flex-col gap-[19px]">
									<span className="w-full font-montserrat font-[600] text-[15px] leading-[18.29px]">
										Invited team
									</span>
									<div className="w-full flex flex-col gap-[15px] ">
										{dummyInviteTeam.members.map((data) => {
											return (
												<div className="w-full flex items-center justify-between py-[4.14px] pl-[11.07px] pr-[16px] h-[45px] bg-white rounded-full">
													<div className="flex items-center gap-[16.79px]">
														<img
															className="h-[36.73px] w-[36.73px]"
															src="/public/group-2864.svg"
															alt=""
														/>
														<span className="font-montserrat font-[500] text-[15px] leading-[18.29px] text-primary-300">
															{data.name}
														</span>
													</div>
													<Ellipsis className="bg-transparent text-primary-300" />
												</div>
											)
										})}
									</div>
								</div>
							</div>
						</div>
					</div>
				) : null}
			</>
		)
};

export default InviteTeam;
