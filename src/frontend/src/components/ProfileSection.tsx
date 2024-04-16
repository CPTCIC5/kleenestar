import { PencilLine } from "lucide-react"
import { useRef } from "react"
import { SubmitHandler, useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import parsePhoneNumber, { CountryCode } from "libphonenumber-js"
import { getNames, registerLocale } from "i18n-iso-countries"
import english from "i18n-iso-countries/langs/en.json"
import CustomSelect from "./CustomSelect"

registerLocale(english)

const countryList = Object.entries(getNames("en")).map(([value, name]) => ({
	value: value, label: name
}))
type FormFields = z.infer<typeof schema>

const schema = z.object({
	first_name: z
		.string()
		.min(5, "The first name should be at least 5 characters long")
		.max(100, "The first name should not exceed 100 characters")
		.regex(/^[a-zA-Z '-]+$/, "Name can only include letters and hypen(-)"),
	last_name: z
		.string()
		.min(5, "The last name should be at least 5 characters long")
		.max(100, "The last name should not exceed 100 characters")
		.regex(/^[a-zA-Z '-]+$/, "Name can only include letters and hypen(-)"),
	email: z.string().email({ message: "Invalid email address" }),
	workspace: z
		.string()
		.min(5, "Workspace name should have atleast 5 characters")
		.max(100, "Workspace length should not exceed 100 characters ")
		.regex(
			/^[a-zA-Z0-9 _-]+$/,
			"Workspace name can include letters, underscores, hypens(-) and numbers only"
		),
	country: z.string().min(1, { message: "Country is required" }),
	number: z.string().min(10, {
		message: "Invalid Phone Number"
	}),
})

function ProfileSection(): JSX.Element {
	const imageRef = useRef<HTMLInputElement>(null)
	const handleAvatarClick = () => {
		if (imageRef.current) {
			imageRef.current.click()
		}
	}

	const form = useForm<FormFields>({
		defaultValues:{
			first_name: "",
			last_name: "",
			email: "",
			workspace: "",
			country: "",
			number:""
		},
		resolver: zodResolver(schema),
		mode: "onChange",
	})
	const { register, handleSubmit, formState, setError, control } = form
	const { errors,isValid } = formState

	const onSubmit: SubmitHandler<FormFields> = (data) => {
		const validPhoneNumber = parsePhoneNumber(
			data.number,
			data.country as CountryCode
		)
		if (
			!validPhoneNumber ||
			!validPhoneNumber.isValid() ||
			!(validPhoneNumber.country === data.country)
		) {
			setError("number", {
				message: "Invalid Phone Number",
			})
			return
		}
		if (!data.country) {
			setError("number", {
				message: "Country Not Selected!",
			})
			return
		}
		console.log(data)
	}

	return (
		<div className="w-[50%] bg-white mq1000:w-[95%] mq1000:mx-auto rounded-[2rem] ">
			<div className="text-primary-300  font-montserrat pt-[28px] pl-8 pb-4 mq1000:pl-4 border-solid border-b-2 border-[#BEB9B1] ">
				<p className=" font-bold text-[16px]"> Profile</p>
				<p className="text-[14px] pt-2  whitespace-nowrap">
					Mange your profile details
				</p>
			</div>
			<div className="py-4 flex items-center gap-4 pl-8 ">
				<div className="w-fit bg-gradient-to-b from-amber-100 to-peach-200 h-fit rounded-full py-[3.5rem] px-[3.6rem] mq1000:px-[2.2rem] mq1000:py-[2.2rem] border-solid border-primary-300 border-4 "></div>
				<div>
					<input
						ref={imageRef}
						className="hidden"
						type="file"
						name="files"
						id=""
					/>
					<img
						onClick={handleAvatarClick}
						src="/add_image.png"
						className="w-[30px] mq1000:w-6"
						alt=""
					/>
				</div>
			</div>
			<div className="p-2 pt-4  w-full font-montserrat text-lg ">
				<div className="w-[95%] mx-auto">
					<div className="flex  justify-center mq1000:flex-col gap-4">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							First name
							<div className="w-full mt-2 bg-background rounded-[2rem] p-4 flex items-center h-[45px] ">
								<input
									{...register("first_name", {
										required: "First Name is required",
									})}
									type="text"
									placeholder="First name"
									className="font-montserrat autofill:bg-transparent bg-clip-text outline-none bg-transparent w-full text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
							{errors.first_name && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.first_name.message}
								</div>
							)}
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Last name
							<div className="w-full mt-2 bg-background h-[45px] rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("last_name", {
										required: "Last Name is required",
									})}
									type="text"
									placeholder="Last name"
									className="autofill:bg-transparent bg-clip-text outline-none bg-transparent w-full font-montserrat  text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
							{errors.last_name && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.last_name.message}
								</div>
							)}
						</div>
					</div>
					<div className="flex  justify-center gap-4 pt-2 mq1000:flex-col">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Email address
							<div className="w-full h-[45px] mt-2 bg-[#D1D3DB] rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("email", {
										required: "Email is required",
									})}
									type="text"
									placeholder="Email address"
									className="autofill:bg-transparent outline-none bg-transparent font-montserrat w-full text-[15px] bg-clip-text"
								/>
								<PencilLine className="text-primary-300 bg-transparent" />
							</div>
							{errors.email && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.email.message}
								</div>
							)}
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Workspace name
							<div className="w-full mt-2 h-[45px] bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("workspace", {
										required: "Workspace name is required",
									})}
									type="text"
									placeholder="Workspace name"
									className="autofill:bg-transparent bg-clip-text outline-none bg-transparent w-full font-montserrat text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
							{errors.workspace && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.workspace.message}
								</div>
							)}
						</div>
					</div>
					<div className="flex  justify-center gap-4 pt-2 mq1000:flex-col">
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Country
							<div className="relative w-full h-[45px] flex items-center mt-2">
								<CustomSelect
									name="country"
									control={control}
									placeholder="Country"
									options={countryList}
								/>
							</div>
							{errors.country && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.country.message}
								</div>
							)}
						</div>
						<div className="w-full text-primary-300 font-bold text-[14px]">
							Phone number
							<div className="w-full h-[45px] mt-2 bg-background rounded-[2rem] p-4 flex items-center ">
								<input
									{...register("number", {
										required: "Phone Number is required",
									})}
									type="text"
									placeholder="Phone number"
									className="autofill:bg-transparent bg-clip-text outline-none bg-transparent w-full font-montserrat text-[15px]"
								/>
								<PencilLine className="text-primary-300" />
							</div>
							{errors.number && (
								<div className="text-red-500 font-[300] text-sm  relative text-right  p-2">
									{errors.number.message}
								</div>
							)}
						</div>
					</div>
					{!isValid && (
						<div className="w-full font-bold rounded-[2rem] cursor-default  bg-opacity-50  my-8  text-white text-[15px]  mq1000:py-[0.7rem] bg-primary-300 text-center py-[10px]">
							Save changes
						</div>
					)}
					{isValid && (
						<div
							onClick={handleSubmit(onSubmit)}
							className="w-full font-bold rounded-[2rem] my-8 cursor-pointer text-white text-[15px]  mq1000:py-[0.7rem] bg-primary-300 text-center py-[10px]">
							Save changes
						</div>
					)}
				</div>
			</div>
		</div>
	)
}

export default ProfileSection
