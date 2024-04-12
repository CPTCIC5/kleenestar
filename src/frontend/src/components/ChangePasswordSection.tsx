import { PencilLine } from "lucide-react";

function ChangePasswordSection(): JSX.Element {
    const password_security_array: Array<number> = [1, 2, 3, 4, 5, 6, 7];
    const current_security: number = 4;
    return (
			<div className="bg-white rounded-[2rem] h-fit pb-4">
				<div className="text-primary-300 pt-[28px]  mq1000:pl-4 font-montserrat pl-8 pb-4  border-solid border-b-2 border-[#BEB9B1] ">
					<p className=" font-bold  text-[18px] mq1000:text-[16px]">
						Change password
					</p>
					<p className="text-[14px] pt-2">
						Change your password will logout of all devices and sessions.
					</p>
				</div>
				<div className=" font-montserrat px-[27.86px]">
					<div className="flex justify-center items-center gap-4 mq1000:pl-2  pt-8 pb-4 mq1000:flex-col">
						<div className="w-full text-primary-300 text-[14px] font-bold ">
							New password
							<div className="w-full h-[45px] mt-2 bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									type="password"
									placeholder="New password"
									className="autofill:bg-transparent outline-none bg-transparent w-full font-montserrat text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
						<div className="w-full text-primary-300 text-[14px] font-bold ">
							Confirm password
							<div className="w-full mt-2 h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									type="password"
									placeholder="Confirm password"
									className="autofill:bg-transparent outline-none bg-transparent w-full font-montserrat text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
						</div>
					</div>
					<div className="flex justify-between px-4 gap-4 mq1000:flex-col text-royalblue">
						<div className="flex gap-2 justify-between mq1000:justify-start ">
							{password_security_array.map((level, index) => {
								return level <= current_security ? (
									<div
										key={index}
										className="w-fit rounded-full bg-royalblue py-[0.4rem] h-fit px-[0.4rem]"></div>
								) : (
									<div
										key={index}
										className="w-fit rounded-full bg-[#E1F0F0] py-[0.4rem] h-fit px-[0.4rem]"></div>
								)
							})}
						</div>
						<div className="text-[13px] text-right mq1000:pt-4">
							Password confirmation matches
						</div>
					</div>
					<div className="w-full text-[15px] mq1000:py-[0.7rem]  font-bold rounded-[2rem] my-8 cursor-pointer text-white bg-primary-300 text-center py-[12px]">
						Change password
					</div>
				</div>
			</div>
		)
}

export default ChangePasswordSection;
