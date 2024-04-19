import { FunctionComponent } from "react";
import { CircleArrowLeft, PencilLine } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import PrimaryButton from "../components/PrimaryButton";
import { zodResolver } from "@hookform/resolvers/zod";
import { FieldValues, SubmitHandler, useForm } from "react-hook-form";
import { z } from "zod";
import CustomSelect from "../components/CustomSelect";
import axios from 'axios'
import {toast} from 'sonner'
import Cookies from 'js-cookie'

const schema = z.object({
    businessName: z.string().nonempty("Business name is required"),
    Website: z
        .string()
        .url({ message: "Invalid URL" })
        .refine((value) => value.includes("."), {
            message: "Website should contain a .",
        }),
    selectedOption: z.string().nonempty("Please select an option"),
});

const OnboardingStep2: FunctionComponent = () => {
    const navigate = useNavigate();

    const {
        register,
        control,
        handleSubmit,

        formState: { errors, isValid },
    } = useForm({
        resolver: zodResolver(schema),
        mode: "onChange",
    });

    const Industries = [
        { value: "Ecommerce", label: "Ecommerce" },
        { value: "Sales", label: "Sales" },
        { value: "Enterprise", label: "Enterprise" },
    ];

    const onSubmit: SubmitHandler<FieldValues> = async(data) => {
        console.log(data);
        try{
        const response =  await axios.patch("http://127.0.0.1:8000/api/workspaces/",{
            business_name: data.businessName,
            website_url:data.Website,
            industry:data.selectedOption
        },{
            withCredentials: true,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': Cookies.get('csrftoken')
            }
        })
        if(response.status === 201){
            toast.success("Workspace Created Successfully!")
        }
        }catch(error){
            console.log(error)
            toast.warning("Faild to create Workspace")
        }
    };

    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4  flex-col gap-[30px]">
            <div className="hidden mq551:block">
                <img src={"/MainLogo.svg"} alt="" />
            </div>
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative bg-white ">
                <div className="absolute top-5 left-5">
                    <CircleArrowLeft onClick={() => navigate(-1)} />
                </div>

                <div className="max-width flex items-center justify-center box-border max-w-full">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
                            Workspace
                        </span>
                        <div className="max-width self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300 flex flex-col">
                            <span>The more Kleenestar knows the better it performs and </span>
                            <span>help your business grow. 🤑</span>
                        </div>
                    </div>
                </div>

                <form
                    method="post"
                    onSubmit={handleSubmit(onSubmit)}
                    className={`max-w-[454px] max-h-[353.99px] w-full  mt-[41px] flex flex-col gap-[16px]`}
                >
                    <div className="w-full h-[72.33px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Business name*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="text"
                                {...register("businessName")}
                                placeholder="Business Name"
                                className={`bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300  text-opacity-50 outline-none focus:outline-primary-100 focus:outline`}
                            />
                            {/* input component for business name*/}
                            <div className="absolute text-primary flex items-center right-4">
                                <PencilLine className="bg-transparent" />
                            </div>
                        </div>
                    </div>
                    <div
                        className={`w-full ${
                            errors.Website ? "h-[114.33px]" : "h-[88.33px]"
                        } gap-[10px] flex flex-col justify-between`}
                    >
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Website*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="url"
                                {...register("Website")}
                                placeholder="https://"
                                className={`bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300  text-opacity-50 outline-none focus:outline-primary-100 focus:outline`}
                            />
                            {/* input component for website*/}
                            <div className="absolute text-primary flex items-center right-4">
                                <PencilLine className="bg-transparent" />
                            </div>
                        </div>

                        {errors.Website && (
                            <div className="w-full h-[16px] flex items-center justify-start">
                                <span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
                                    {typeof errors.Website.message === "string"
                                        ? errors.Website.message
                                        : null}
                                </span>
                            </div>
                        )}
                    </div>
                    <div className="w-full h-[72 .3px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Industry
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <CustomSelect
                                name={"selectedOption"}
                                control={control}
                                placeholder="Answer"
                                options={Industries}
                            />
                        </div>
                    </div>
                    <div className="h-[40px] max-w-[454px] w-full mt-[17px]">
                        <PrimaryButton disabled={!isValid}>Create</PrimaryButton>
                        {/* Use the PrimaryButton component */}
                    </div>
                </form>

                <div className="max-w-[435px] h-[37px] w-full flex justify-center mt-[39px]">
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

export default OnboardingStep2;
