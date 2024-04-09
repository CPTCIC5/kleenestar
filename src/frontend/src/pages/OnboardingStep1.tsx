import { FunctionComponent } from "react";
import { Link } from "react-router-dom";
import { MoveRight } from "lucide-react";
import PrimaryButton from "../components/PrimaryButton";

const OnboardingStep1: FunctionComponent = () => {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4 flex-col gap-[30px]">
            <div className="hidden mq551:block">
                <img src={"/public/MainLogo.svg"} alt="" />
            </div>
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 bg-white">
                <div className="max-width flex items-center justify-center box-border max-w-full">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
                            Get Started
                        </span>
                        <div className="max-width self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300 flex">
                            <span>A new way to run highly efficient marketing analytics </span>
                            <span>across channels and learn real-time insights 🚀</span>
                        </div>
                    </div>
                </div>

                <div className="mt-[41px] max-w-[454px] w-full h-[40px] ">
                    <Link to={"/OnboardingStep1"} className="no-underline">
                        <PrimaryButton className="flex items-center justify-center gap-[10px]">
                            <span className="bg-primary-300 text-white">Create a workspace</span>
                            <MoveRight className="bg-primary-300 text-white" />
                        </PrimaryButton>
                    </Link>
                    {/* PrimaryButton for create workspace */}
                </div>

                <div className="h-[17px] w-full flex justify-center mt-[39px]">
                    <span className="h-[17px] font-montserrat text-[14px] font-[400] leading-[17.07px] text-center">
                        Already using KleeneStar?{" "}
                        <Link to={"/"} className="underline text-black">
                            Log in to an existing workspace
                        </Link>
                        {/* Link to login page */}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default OnboardingStep1;
