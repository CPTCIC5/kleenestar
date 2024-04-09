import { PencilLine } from "lucide-react";

function ChangePasswordSection(): JSX.Element {
    const password_security_array: Array<number> = [1, 2, 3, 4, 5, 6, 7];
    const current_security: number = 4;
    return (
        <div className="bg-white rounded-[2rem] h-fit pb-4">
            <div className="text-primary-300 mq750:pl-4 font-montserrat pt-2 pl-8 pb-4  border-solid border-b-2 border-[#BEB9B1] ">
                <p className=" font-bold text-[1.6rem] mq750:text-[16px]">Change password</p>
                <p className="mq750:text-[14px]">
                    Change your password will logout of all devices and sessions.
                </p>
            </div>
            <div className="w-[95%] font-montserrat mx-auto">
                <div className="flex justify-center items-center gap-4 mq750:pl-2  pt-8 pb-4 mq750:flex-col">
                    <div className="w-full text-primary-300 mq750:text-[14px] font-bold text-xl">
                        New password
                        <div className="w-full mq750:h-[45px] mt-2 bg-background rounded-[2rem] p-4 flex items-center ">
                            <input
                                type="password"
                                placeholder="New password"
                                className="w-full font-montserrat text-xl mq750:text-[15px]"
                            />
                            <PencilLine className="text-primary-300" />
                        </div>
                    </div>
                    <div className="w-full text-primary-300 mq750:text-[14px] font-bold text-xl">
                        Confirm password
                        <div className="w-full mt-2 mq750:h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
                            <input
                                type="password"
                                placeholder="Confirm password"
                                className="w-full font-montserrat text-xl mq750:text-[15px]"
                            />
                            <PencilLine className="text-primary-300" />
                        </div>
                    </div>
                </div>
                <div className="flex justify-between px-4 gap-4 mq750:flex-col text-royalblue">
                    <div className="flex gap-4 ">
                        {password_security_array.map((level, index) => {
                            return level <= current_security ? (
                                <div
                                    key={index}
                                    className="w-fit rounded-full bg-royalblue py-[0.4rem] h-fit px-[0.4rem]"
                                ></div>
                            ) : (
                                <div
                                    key={index}
                                    className="w-fit rounded-full bg-[#E1F0F0] py-[0.4rem] h-fit px-[0.4rem]"
                                ></div>
                            );
                        })}
                    </div>
                    <div className="mq750:text-[13px] mq750:pt-4">
                        Password confirmation matches
                    </div>
                </div>
                <div className="w-full mq750:text-[15px] mq750:py-[0.7rem] font-bold rounded-[2rem] my-8 cursor-pointer text-white bg-primary-300 text-center py-[1rem]">
                    Change password
                </div>
            </div>
        </div>
    );
}

export default ChangePasswordSection;
