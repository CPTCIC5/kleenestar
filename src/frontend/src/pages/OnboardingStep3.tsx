import { FunctionComponent, useEffect, useState } from "react";
import GoogleOauthButton from "../components/GoogleOauthButton";
import { Circle, CircleArrowLeft, Eye, EyeOff, PencilLine } from "lucide-react";
import { useNavigate } from "react-router-dom";
import PrimaryButton from "../components/PrimaryButton";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Controller } from "react-hook-form";

const schema = z.object({
    email: z.string().email(),
    password: z
        .string()
        .min(8, { message: "Password must be at least 8 characters long" })
        .refine((value) => /[a-z]/.test(value), {
            message: "Password must contain a lowercase letter",
        })
        .refine((value) => /[A-Z]/.test(value), {
            message: "Password must contain an uppercase letter",
        })
        .refine((value) => /\d/.test(value), { message: "Password must contain a number" })
        .refine((value) => /[@$!%*?&]/.test(value), {
            message: "Password must contain a special character",
        }),
    confirmPassword: z.string().min(8),
    newsletter: z.boolean(),
});

type FormData = z.infer<typeof schema>;

const OnboardingStep3: FunctionComponent = () => {
    const navigate = useNavigate();
    const {
        control,
        handleSubmit,
        register,
        formState: { errors, isValid },
        watch,
        setError,
        clearErrors,
    } = useForm<FormData>({
        resolver: zodResolver(schema),
        mode: "onChange",
    });

    const [passwordShow1, setPasswordShow1] = useState<boolean>(false);
    const [passwordShow2, setPasswordShow2] = useState<boolean>(false);
    const [passwordUnmatch, setPasswordUnmatch] = useState<boolean>(false);

    // Watch for changes in password and confirmPassword
    const password = watch("password");
    const confirmPassword = watch("confirmPassword");

    useEffect(() => {
        if (password === confirmPassword) {
            setPasswordUnmatch(false);
            clearErrors("confirmPassword");
        }
    }, [password, confirmPassword, clearErrors]);

    const onSubmit = (data: FormData) => {
        if (data.password !== data.confirmPassword) {
            setPasswordUnmatch(true);
            setError("confirmPassword", {
                type: "manual",
                message: "Passwords do not match",
            });
        } else {
            console.log(data);
        }
    };

    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4 flex-col gap-[30px]">
            <div className="hidden mq551:block">
                <img src={"/public/MainLogo.svg"} alt="" />
            </div>
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative bg-white ">
                <div className="absolute top-5 left-5">
                    <CircleArrowLeft onClick={() => navigate(-1)} />
                </div>

                <div className="max-width flex items-center justify-center box-border max-w-full">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
                            Account
                        </span>
                        <span className="max-width self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300">
                            We suggest using the email address you use at work.
                        </span>
                    </div>
                </div>

                <form
                    method="post"
                    onSubmit={handleSubmit(onSubmit)}
                    className={`max-w-[454px] w-full max-h-[434px] mt-[50.05px] flex flex-col items-center gap-[16px]`}
                >
                    <div
                        className={`w-full  ${
                            errors.email ? "h-[99.66px]" : "h-[73.66px]"
                        } gap-[10px] flex flex-col justify-between`}
                    >
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Email*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="email"
                                {...register("email")}
                                placeholder="@work-email.com"
                                className={`bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300  text-opacity-50 outline-none focus:outline-primary-100 focus:outline`}
                            />
                            <div className="absolute bg-background text-primary flex items-center right-4">
                                <PencilLine className="bg-inherit" />
                            </div>
                        </div>

                        {errors.email && (
                            <div className="w-full h-[16px] flex items-center justify-start">
                                <span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
                                    Unauthorized email
                                </span>
                            </div>
                        )}
                    </div>
                    <div className="w-full h-[72.33px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Password*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type={passwordShow1 ? "text" : "password"}
                                placeholder="Password"
                                {...register("password")}
                                className={`bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300  text-opacity-50 outline-none focus:outline-primary-100 focus:outline`}
                            />
                            {/*input component for password*/}
                            <div
                                onClick={() => setPasswordShow1(!passwordShow1)}
                                className="absolute bg-background text-primary flex items-center right-4 cursor-pointer"
                            >
                                {passwordShow1 ? (
                                    <EyeOff className="bg-inherit" />
                                ) : (
                                    <Eye className="bg-inherit" />
                                )}
                            </div>
                        </div>
                    </div>
                    <div
                        className={`w-full  ${
                            passwordUnmatch || errors.password ? "h-[99.66px]" : "h-[73.66px]"
                        } gap-[10px] flex flex-col justify-between`}
                    >
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Confirm Password*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type={passwordShow2 ? "text" : "password"}
                                placeholder="Confirm Password"
                                {...register("confirmPassword")}
                                className={`bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300  text-opacity-50 outline-none focus:outline-primary-100 focus:outline`}
                            />
                            {/*input component for password*/}
                            <div
                                onClick={() => setPasswordShow2(!passwordShow2)}
                                className="absolute bg-background text-primary flex items-center right-4 cursor-pointer"
                            >
                                {passwordShow2 ? (
                                    <EyeOff className="bg-inherit" />
                                ) : (
                                    <Eye className="bg-inherit" />
                                )}
                            </div>
                        </div>

                        {(passwordUnmatch || errors.password) && (
                            <div className="w-full h-[16pxpx] flex items-center justify-start">
                                <span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
                                    {errors.password
                                        ? errors.password.message
                                        : passwordUnmatch
                                        ? "Password doesn't match"
                                        : ""}
                                </span>
                            </div>
                        )}
                    </div>
                    <div className="h-[19px] max-w-[330px] w-full flex items-center justify-center gap-1 mt-[3px]">
                        <Controller
                            control={control}
                            name="newsletter"
                            defaultValue={true}
                            render={({ field }) => (
                                <div className="flex" onClick={() => field.onChange(!field.value)}>
                                    {field.value ? (
                                        <Circle fill={"#495270"} size={"16px"} />
                                    ) : (
                                        <Circle size={"16px"} />
                                    )}
                                </div>
                            )}
                        />
                        <span className="h-[17px] font-montserrat font-[400] text-[14px] leading-[17.07px]">
                            Send me emails with tips, news, and offers.
                        </span>
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

export default OnboardingStep3;
