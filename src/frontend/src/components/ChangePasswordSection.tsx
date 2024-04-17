import { EyeOff } from "lucide-react";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { SubmitHandler, useForm } from "react-hook-form";
import { ChangeEvent, useEffect, useState } from "react";
import Cookies from "js-cookie"
import axios,{AxiosError} from 'axios'



const schema = z.object({
	password: z
		.string()
		.min(8, { message: "Password must be at least 8 characters long" })
		.refine((value) => /[a-z]/.test(value), {
			message: "Password must contain a lowercase letter",
		})
		.refine((value) => /[A-Z]/.test(value), {
			message: "Password must contain an uppercase letter",
		})
		.refine((value) => /\d/.test(value), {
			message: "Password must contain a number",
		})
		.refine((value) => /[@$!%*?&]/.test(value), {
			message: "Password must contain a special character",
		}),
	confirmPassword: z
		.string()
		.min(8, {
			message: "Confirm Password should be atleast 8 characters long",
		}),
	currentPassword: z
		.string()
		.min(8, {
			message: "Current Password should be atleast 8 characters long",
		}), 
})
type FormFields = z.infer<typeof schema>;

function ChangePasswordSection(): JSX.Element {

    useEffect(()=>{

    },[])

    const calculateSecurity = (password: string) => {
        let security = 0;

        if (password.length >= 8) {
            security++;
        }

        if (/\d/.test(password)) {
            security++;
        }

        if (/[a-z]/.test(password)) {
            security++;
        }

        if (/[A-Z]/.test(password)) {
            security++;
        }

        if (/[!@#$%^&*]/.test(password)) {
            security++;
        }

        return security;
    };
    const password_security_array: Array<number> = [1, 2, 3, 4, 5];
    const [passwordValue, setPasswordValue] = useState("");
    const [current_security, setCurrentSecurity] = useState(0);
    useEffect(() => {
        setCurrentSecurity(calculateSecurity(passwordValue));
    }, [passwordValue]);
    const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
        setPasswordValue(event.target.value);
    };

    const { register, handleSubmit, setError, formState, watch, clearErrors } =
			useForm<FormFields>({
				defaultValues: {
					password: "",
					confirmPassword: "",
					currentPassword: "",
				},
				resolver: zodResolver(schema),
				mode: "onChange",
			})
    const onSubmit: SubmitHandler<FormFields> = async(data) => {
        if (data.password !== data.confirmPassword) {
            setPasswordMatch(false);
            setError("confirmPassword", {
                message: "Password confirmation does not match!",
            });
            return;
        }

        const CSRFToken = Cookies.get("csrftoken")
        console.log(CSRFToken)
        try{
            const response = await axios.post("http://127.0.0.1:8000/api/auth/change-password/",{
                current_password: data.currentPassword,
                new_password: data.password,
                confirm_new_password:data.confirmPassword
            },{
                headers: {
                    "X-CSRFToken" : CSRFToken,
                    "Content-Type":  "application/json"
                }
            })
            if(response.status == 200){
                console.log("Done", response)
            }
        }
        catch(error){
            const err = error as AxiosError
            console.log(err)
        }
    };
    const [passwordMatch, setPasswordMatch] = useState<boolean>(false);
    const password = watch("password");
    const confirmPassword = watch("confirmPassword");
    useEffect(() => {
        if (password === confirmPassword && password !== "" && confirmPassword !== "") {
            setPasswordMatch(true);
            clearErrors("confirmPassword");
        }
    }, [password, confirmPassword, clearErrors]);
    const { errors, isValid } = formState;
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
					<div className="flex justify-center  gap-4 mq1000:pl-2  pt-8 mq1000:flex-col">
						<div className="w-full text-primary-300 text-[14px] font-bold ">
							Current password
							<div className="w-full mt-2 h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("currentPassword", {
										required: "Confirm Password is Required",
									})}
									type="password"
									placeholder="Current password"
									className="autofill:bg-transparent outline-none bg-transparent bg-clip-text w-full font-montserrat text-[15px]"
								/>
								<EyeOff className="text-primary-300" />
							</div>
							{errors.currentPassword && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.currentPassword?.message ?? ""}
								</div>
							)}
						</div>
					</div>
					<div className="flex justify-center  gap-4 mq1000:pl-2  pt-8 pb-4 mq1000:flex-col">
						<div className="w-full text-primary-300 text-[14px] font-bold ">
							New password
							<div className="w-full h-[45px] mt-2 bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("password", {
										required: "Password is Required",
									})}
									type="password"
									placeholder="New password"
									onChange={(event) => {
										handlePasswordChange(event)
										register("password").onChange(event)
									}}
									className="autofill:bg-transparent outline-none bg-transparent w-full bg-clip-text font-montserrat text-[15px]"
								/>
								<EyeOff className="text-primary-300" />
							</div>
							{errors.password && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.password.message}
								</div>
							)}
						</div>
						<div className="w-full text-primary-300 text-[14px] font-bold ">
							Confirm password
							<div className="w-full mt-2 h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("confirmPassword", {
										required: "Confirm Password is Required",
									})}
									type="password"
									placeholder="Confirm password"
									className="autofill:bg-transparent outline-none bg-transparent bg-clip-text w-full font-montserrat text-[15px]"
								/>
								<EyeOff className="text-primary-300" />
							</div>
							{errors.confirmPassword && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.confirmPassword?.message ?? ""}
								</div>
							)}
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

						{passwordMatch && isValid && (
							<div className="text-[13px] text-right mq1000:pt-4">
								{"Password confirmation matches"}
							</div>
						)}
					</div>
					{!isValid && (
						<div className="w-full font-bold rounded-[2rem] cursor-default  bg-opacity-50  my-8  text-white text-[15px]  mq1000:py-[0.7rem] bg-primary-300 text-center py-[10px]">
							Change password
						</div>
					)}
					{isValid && (
						<div
							onClick={handleSubmit(onSubmit)}
							className="w-full font-bold rounded-[2rem] my-8 cursor-pointer text-white text-[15px]  mq1000:py-[0.7rem] bg-primary-300 text-center py-[10px]">
							Change password
						</div>
					)}
				</div>
			</div>
		)
}

export default ChangePasswordSection;
