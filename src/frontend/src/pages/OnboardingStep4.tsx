import { FunctionComponent } from "react";
import GoogleOauthButton from "../components/GoogleOauthButton";
import { CircleArrowLeft, CircleHelp, PencilLine } from "lucide-react";
import { useNavigate } from "react-router-dom";
import PrimaryButton from "../components/PrimaryButton";
import { FieldValues, SubmitHandler, useForm } from "react-hook-form";
import CustomSelect from "../components/CustomSelect";

const OnboardingStep4: FunctionComponent = () => {
    const navigate = useNavigate();
    const {
        register,
        control,
        handleSubmit,
        formState: { isValid },
    } = useForm({
        mode: "onChange",
    });

    const BusinessSize = [
        { value: "startup", label: "startup" },
        { value: "growth", label: "growth" },
        { value: "maturity", label: "maturity" },
    ];

    const BusinessObjectives = [
        { value: "apple", label: "Apple" },
        { value: "banana", label: "Banana" },
        { value: "orange", label: "Orange" },
    ];

    const onSubmit: SubmitHandler<FieldValues> = (data) => {
        console.log(data);
    };

    return (
        <div className="w-full min-h-screen h-full flex items-center justify-center bg-background p-4 flex-col gap-[30px]">
            <div className="hidden mq551:block">
                <img src={"/public/MainLogo.svg"} alt="" />
            </div>
            <div className="max-w-[722px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative bg-white ">
                <div className="absolute top-5 left-5">
                    <CircleArrowLeft onClick={() => navigate(-1)} />
                </div>

                <div className="max-width flex items-center justify-center box-border max-w-full">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
                            Almost There
                        </span>
                        <span className="max-w-[454px] w-full self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300">
                            A few questions to help Kleenestar better assist you with explosive
                            growth.
                        </span>
                    </div>
                </div>

                <form
                    method="post"
                    onSubmit={handleSubmit(onSubmit)}
                    className={`max-w-[454px] w-full mt-[50.05px] flex flex-col items-center gap-[18px]`}
                >
                    <div className="max-w-[454px] w-full flex flex-col gap-[9px]">
                        <div className="w-full flex flex-row justify-between items-center">
                            <div className="max-w-[378px] w-full font-montserrat font-[600] text-[14px] leading-[18px] text-primary-300 ">
                                What is the size of your business, and what stage is it currently in
                                (startup, growth, maturity)?
                            </div>
                            <CircleHelp className="h-[20.88px] w-[20.88px] bg-transparent text-primary-300" />
                        </div>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <CustomSelect
                                name="BusinessSize"
                                control={control}
                                placeholder="Answer"
                                options={BusinessSize}
                            />
                        </div>
                    </div>
                    <div className="max-w-[454px] w-full flex flex-col gap-[9px]">
                        <div className="w-full flex flex-row justify-between items-center">
                            <div className="max-w-[378px] w-full font-montserrat font-[600] text-[14px] leading-[18px] text-primary-300 ">
                                What are your primary business objectives for the next 6-12 months?
                            </div>
                            <CircleHelp className="h-[20.88px] w-[20.88px] bg-transparent text-primary-300" />
                        </div>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <CustomSelect
                                name="BusinessObjectives"
                                control={control}
                                placeholder="Answer"
                                options={BusinessObjectives}
                            />
                        </div>
                    </div>
                    <div className="max-w-[454px] w-full flex flex-col gap-[9px]">
                        <div className="w-full flex flex-row justify-between items-center">
                            <div className="max-w-[378px] w-full font-montserrat font-[600] text-[14px] leading-[18px] text-primary-300 ">
                                What are your main challenges when it comes to data analysis and
                                decision-making in your marketing efforts?
                            </div>
                            <CircleHelp className="h-[20.88px] w-[20.88px] bg-transparent text-primary-300" />
                        </div>
                        <div className="relative w-full min-h-[51px] flex items-center ">
                            <textarea
                                {...register("textareaFieldName", { required: true })}
                                placeholder="Answer"
                                className="bg-background rounded-t-3xl rounded-b-3xl w-full h-full px-4  pr-10 py-4 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300 outline-none focus:outline-primary-100 focus:outline resize-y"
                            />
                            {/* PrimaryInputBox component for note*/}
                            <div className="absolute bg-background text-primary flex items-center right-4 bottom-4">
                                <PencilLine className="bg-inherit" />
                            </div>
                        </div>
                    </div>
                    <div className="h-[40px] max-w-[454px] w-full mt-[23px]">
                        <PrimaryButton disabled={!isValid}>Continue</PrimaryButton>
                        {/* Use the PrimaryButton component */}
                    </div>
                </form>

                <div className="max-w-[454px] w-full h-[40px] flex justify-center mt-[25.25px] items-center ">
                    <GoogleOauthButton /> {/* Use the GoogleOauthButton component */}
                </div>
            </div>
        </div>
    );
};

export default OnboardingStep4;
