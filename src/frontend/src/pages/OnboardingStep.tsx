import { FunctionComponent } from "react";
import BusinessNameContainer from "../components/BusinessNameContainer";
import RoundArrowRightSvgrepoCom from "../components/RoundArrowRightSvgrepoCom";
import RoundArrowRightSvgrepoCom1 from "../components/RoundArrowRightSvgrepoCom1";

const OnboardingStep: FunctionComponent = () => {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4">
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative ">
                <div className="absolute top-5 left-5">
                    <RoundArrowRightSvgrepoCom1 />
                </div>
                <div className="max-width flex items-center justify-center box-border max-w-full text-11xl font-syne">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className=" m-0 text-inherit font-bold font-inherit inline-block z-[1]">
                            Workspace
                        </span>
                        <div className="max-width self-stretch text-base text-center font-montserrat z-[1] flex flex-col item-center">
                            <span>The more Kleenestar knows the better it performs and </span>
                            <span>help your business grow. 🤑</span>
                        </div>
                    </div>
                </div>

                <div className="max-w-[454px] w-full h-[248.99px] mt-[59.05px] flex flex-col gap-[16px]">
                    <div className="w-full h-[72.33px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Business name*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="text"
                                name="business_name"
                                placeholder="Business name"
                                className="bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary  text-opacity-50 outline-none"
                                required
                            />
                            <img
                                className="absolute bg-background flex items-center right-4"
                                alt=""
                                src="/pen2svgrepocom1.svg"
                            />
                        </div>
                    </div>
                    <div className="w-full h-[72.33px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Website*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="url"
                                name="website"
                                placeholder="https://"
                                className="bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary  text-opacity-50 outline-none"
                                required
                            />
                            <img
                                className="absolute bg-background flex items-center right-4"
                                alt=""
                                src="/pen2svgrepocom1.svg"
                            />
                        </div>
                    </div>
                    <div className="w-full h-[99.3px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Industry
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="text"
                                placeholder="What’s your industry?"
                                name="password"
                                className="bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary  text-opacity-50 outline-none"
                                required
                            />
                            <img
                                className="absolute bg-background flex items-center right-4"
                                alt=""
                                src="/altarrowdownsvgrepocom.svg"
                            />
                        </div>
                    </div>
                </div>
                <button className="cursor-pointer bg-primary-300 text-white rounded-full w-full h-[40px] shrink-0 border-none p-0 self-stretch position-relative max-w-[454px] mx-auto font-montserrat font-[600] text-[15px] leading-[18.29px] text-center mt-[39px]">
                    Create
                </button>

                <div className="max-w-[435px] h-[37px] w-full flex justify-center mt-[46.26px]">
                    <span className="font-montserrat text-[14px] font-[400]  text-center">
                        By continuing, you’re agreeing to our{" "}
                        <span className="underline">Terms of Service</span>,{" "}
                        <span className="underline">Privacy Policy</span>,{" and "}
                        <span className="underline"> Cookie Policy.</span>
                    </span>
                </div>
            </div>
        </div>
    );
};

export default OnboardingStep;
