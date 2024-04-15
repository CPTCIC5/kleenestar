import { FunctionComponent, useState } from "react"
import GoogleOauthButton from "../components/GoogleOauthButton"
import PrimaryButton from "../components/PrimaryButton"
import { Link } from "react-router-dom"
import { Eye, EyeOff, PencilLine } from "lucide-react"
import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { SubmitHandler, useForm } from "react-hook-form"
import axios from "axios"

const schema = z.object({
	email: z.string().email({ message: "Unauthorized email" }),
	password: z
		.string()
		.min(8, { message: "Password must be at least 8 characters long" }),
})

type FormFields = z.infer<typeof schema>

const Login: FunctionComponent = () => {
	const [passwordShow, setPasswordShow] = useState<boolean>(false)

	const { handleSubmit, register, formState, setError, clearErrors } = useForm<FormFields>({
		defaultValues: {
			email: "",
			password: "",
		},
		resolver: zodResolver(schema),
		mode: "onChange",
	})
	const { errors, isValid } = formState
	const onSubmit: SubmitHandler<FormFields> = async (data) => {
		console.log(data)
		const { email, password } = data
		try {
			const response = await axios.post(
				"http://127.0.0.1:8000/api/auth/login/",
				{
					email: email,
					password: password,
				}
			)
			console.log(response.data) // Do something with the response
            clearErrors("password")
			alert("Logged In!")
		} catch (error) {
			setError("password",{
                message: String(error)
            })
			console.error("Error submitting the form:", error)
		}
	}
	return (
		<div className="w-full h-screen flex items-center justify-center bg-background p-4  flex-col gap-[30px]">
			<div className="hidden mq551:block">
				<img
					src={"/public/MainLogo.svg"}
					alt=""
				/>
			</div>
			<div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 bg-white">
				<div className="max-width flex items-center justify-center box-border max-w-full">
					<div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
						<span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
							Welcome back
						</span>
						<span className="max-width self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300">
							Welcome back, log in to your workspace
						</span>
					</div>
				</div>

				<form
					method="post"
					onSubmit={handleSubmit(onSubmit)}
					className={`max-w-[454px] max-h-[292.63px] w-full mt-[39px] flex flex-col gap-[16px]`}>
					<div
						className={`w-full ${
							errors.email ? "h-[98.33px]" : "h-[72.33px]"
						} gap-[10px] flex flex-col justify-between`}>
						<span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
							Email*
						</span>
						<div className="relative w-full h-[45px] flex items-center ">
							<input
								{...register("email", {
									required: "Email is Required",
								})}
								type="email"
								name="email"
								placeholder="my@email.com"
								className="`bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300  text-opacity-50 outline-none bg-clip-text focus:outline-primary-100 focus:outline`"
							/>
							{/* input component for email*/}
							<div className="absolute bg-background text-primary flex items-center right-4">
								<PencilLine className="bg-inherit " />
							</div>
						</div>
						{errors.email && (
							<div className="w-full h-[16px] flex items-center justify-start">
								<span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
									{errors.email.message}
								</span>
							</div>
						)}
					</div>

					<div className="w-full h-[99.3px] gap-[10px] flex flex-col justify-between">
						<span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
							Password*
						</span>
						<div className="relative w-full h-[45px] flex items-center ">
							<input
								{...register("password", {
									required: "Password is Required",
								})}
								type={passwordShow ? "text" : "password"}
								placeholder="Password"
								name="password"
								className="bg-background bg-clip-text rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300  text-opacity-50 outline-none focus:outline-primary-100 focus:outline"
							/>
							{/*input component for password*/}
							<div
								onClick={() => setPasswordShow(!passwordShow)}
								className="absolute bg-background text-primary flex items-center right-4 cursor-pointer">
								{passwordShow ? (
									<EyeOff className="bg-inherit" />
								) : (
									<Eye className="bg-inherit" />
								)}
							</div>
						</div>

						<div
							className={`w-full h-[16px] flex items-center ${
								errors.password ? "justify-between" : "justify-end"
							}`}>
							{errors.password && (
								<span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
									{errors.password.message}
								</span>
							)}

							<Link
								to={"/forgot-password"}
								className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-slategray underline">
								Forgot password?
							</Link>
							{/* forgot-password link */}
						</div>
					</div>
					<div className="h-[40px] max-w-[454px] w-full mt-[23px]">
						<PrimaryButton disabled={!isValid}>Login</PrimaryButton>
						{/* Use the PrimaryButton component */}
					</div>
				</form>

				<div className="max-w-[454px] w-full h-[40px] flex justify-center mt-[25.25px] items-center ">
					<GoogleOauthButton /> {/* Use the GoogleOauthButton component */}
				</div>

				<div className="h-[25.47px] w-full flex justify-center mt-[46.27px]">
					<span className="h-[17px] font-montserrat text-[14px] font-[400] leading-[10.07px] text-center">
						Need a workspace?
						<Link
							to={"/onboard/step2"}
							className="underline text-black">
							Create a workspace
						</Link>
						{/* create-workspace link */}
					</span>
				</div>
			</div>
		</div>
	)
}

export default Login
