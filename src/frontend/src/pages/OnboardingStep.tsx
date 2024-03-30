import { FunctionComponent } from "react";
import { ChevronDown, CircleArrowLeft, PencilLine } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import PrimaryInputBox from "../components/PrimaryInputBox";
import PrimaryButton from "../components/PrimaryButton";

const OnboardingStep: FunctionComponent = () => {
    const navigate = useNavigate();

    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4">
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative ">
                <div className="absolute top-5 left-5">
                    <CircleArrowLeft onClick={() => navigate(-1)} />
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
                            <PrimaryInputBox
                                type="text"
                                name="business_name"
                                placeholder="Business name"
                                className="focus:outline-primary-100 focus:outline"
                                required
                            />
                            <div className="absolute bg-background text-primary flex items-center right-4">
                                <PencilLine className="bg-inherit" />
                            </div>
                        </div>
                    </div>
                    <div className="w-full h-[72.33px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Website*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <PrimaryInputBox
                                type="url"
                                name="Website"
                                placeholder="https://"
                                className="focus:outline-primary-100 focus:outline"
                                required
                            />
                            {/* PrimaryInputBox component for website*/}
                            <div className="absolute bg-background text-primary flex items-center right-4">
                                <PencilLine className="bg-inherit" />
                            </div>
                        </div>
                    </div>
                    <div className="w-full h-[99.3px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Industry
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <PrimaryInputBox
                                type="text"
                                name="industy"
                                placeholder="What’s your industry?"
                                className="focus:outline-primary-100 focus:outline"
                                required
                            />
                            {/* PrimaryInputBox component for email*/}
                            <div className="absolute bg-background text-primary flex items-center right-4">
                                <ChevronDown className="bg-inherit" />
                            </div>
                        </div>
                    </div>
                </div>

                <div className="h-[40px] max-w-[454px] w-full mt-[39px]">
                    <PrimaryButton>Create</PrimaryButton> {/* Use the PrimaryButton component */}
                </div>

                <div className="max-w-[435px] h-[37px] w-full flex justify-center mt-[46.26px]">
                    <span className="font-montserrat text-[14px] font-[400]  text-center">
                        By continuing, you’re agreeing to our{" "}
                        <Link to={"/terms-of-condition"} className="underline text-primary-300">
                            Terms of Service
                        </Link>
                        ,{" "}
                        <Link to={"/privacy-policy"} className="underline text-primary-300">
                            Privacy Policy
                        </Link>
                        ,{" and "}
                        <Link to={"/cookie-policy"} className="underline text-primary-300">
                            {" "}
                            Cookie Policy.
                        </Link>
                    </span>
                </div>
            </div>
        </div>
    );
};

export default OnboardingStep;
