import { FunctionComponent} from "react";
import { PencilLine } from "lucide-react";
import PrimaryButton from "../components/PrimaryButton";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

const schema = z.object({
    email: z.string().email(),
});

type FormData = z.infer<typeof schema>;

const RecoveryEmail: FunctionComponent = () => {
    const {
        handleSubmit,
        register,
        formState: { errors, isValid },
    } = useForm<FormData>({
        resolver: zodResolver(schema),
        mode: "onChange",
    });

    const onSubmit = (data: FormData) => {
        console.log(data);
    };

    const handleSendCode = () => {
        {
            /* add send code request here */
        }
    };

    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4 flex-col gap-[30px]">
            <div className=" items-center justify-center gap-[18.13px] flex">
                <img className="w-[52.07px] h-[54.78px]" src="/group-672.svg" alt="" />
                <span className="w-[156.02px] font-syne font-[700] text-[25px] leading-[30px]">
                    Kleenestar
                </span>
            </div>
            <div className="max-w-[722px] max-h-[531.66px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative bg-white">
                <div className="max-width flex items-center justify-center box-border max-w-full">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
                            Recovery Email
                        </span>
                        <span className="max-w-[454px] w-full self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300">
                            Send a password recovery email to your registered email address. 💁
                        </span>
                    </div>
                </div>

                <form
                    method="post"
                    onSubmit={handleSubmit(onSubmit)}
                    className={`max-w-[454px] w-full max-h-[434px] mt-[39px] flex flex-col items-center gap-[16px]`}
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
                                    Email not recognized
                                </span>
                            </div>
                        )}
                    </div>
                    <div className="h-[40px] max-w-[454px] w-full mt-[23px]">
                        <PrimaryButton disabled={!isValid}>Send email</PrimaryButton>
                        {/* Use the PrimaryButton component */}
                    </div>
                </form>

                <div className="h-[25.47px] w-full flex justify-center mt-[30px]">
                    <span className="h-[17px] font-montserrat text-[14px] font-[400] leading-[10.07px] text-center">
                        Did not receive a code?
                        <span
                            onClick={handleSendCode}
                            className="underline text-black cursor-pointer"
                        >
                            Send code
                        </span>
                        {/* send code link */}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default RecoveryEmail;
