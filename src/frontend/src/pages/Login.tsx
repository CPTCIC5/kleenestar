
import { FunctionComponent } from "react";
import React, { useState } from "react";
import axios from "axios";
import GoogleOauthButton from "../components/GoogleOauthButton";
import PrimaryButton from "../components/PrimaryButton";
import PrimaryInputBox from "../components/PrimaryInputBox";
import { Link } from "react-router-dom";
import { Eye, EyeOff, PencilLine } from "lucide-react";

interface FormData {
    email: string;
    password: string;
}
const Login: FunctionComponent = () => {
    const [passwordShow, setPasswordShow] = useState<boolean>(false);
    const [incorrectCredentials, setIncorrectCredentials] = useState<boolean>(false);

    const [formData, setFormData] = useState<FormData>({
        email: "",
        password: "",
    });

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/auth/login/", {
                email: formData.email,
                password: formData.password,
            });
            console.log(response.data); // Do something with the response
            alert("Logged In!");
            setIncorrectCredentials(false);
        } catch (error) {
            setIncorrectCredentials(true);
            console.error("Error submitting the form:", error);
        }
    };

    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4">
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4">
                <div className="max-width flex items-center justify-center box-border max-w-full text-11xl font-syne">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className=" m-0 text-inherit font-bold font-inherit inline-block z-[1]">
                            Welcome back
                        </span>
                        <span className="max-width self-stretch text-base text-center font-montserrat z-[1]">
                            Welcome back, log in to your workspace
                        </span>
                    </div>
                </div>

                <form
                    method="post"
                    onSubmit={handleSubmit}
                    className="max-w-[454px] w-full h-[187.63px] mt-[59.05px] flex flex-col gap-[16px]"
                >
                    <div className="w-full h-[72.33px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Email*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <PrimaryInputBox
                                type="email"
                                name="email"
                                placeholder="my@email.com"
                                onChange={handleInputChange}
                                className="focus:outline-primary-100 focus:outline"
                                value={formData.email}
                                required
                            />
                            {/* PrimaryInputBox component for email*/}
                            <div className="absolute bg-background text-primary flex items-center right-4">
                                <PencilLine className="bg-inherit" />
                            </div>
                        </div>
                    </div>
                    <div className="w-full h-[99.3px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Password*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <PrimaryInputBox
                                type={passwordShow ? "text" : "password"}
                                placeholder="Password"
                                name="password"
                                onChange={handleInputChange}
                                className="focus:outline-primary-100 focus:outline"
                                value={formData.password}
                                required
                            />
                            {/*PrimaryInputBox component for password*/}
                            <div
                                onClick={() => setPasswordShow(!passwordShow)}
                                className="absolute bg-background text-primary flex items-center right-4 cursor-pointer"
                            >
                                {passwordShow ? (
                                    <EyeOff className="bg-inherit" />
                                ) : (
                                    <Eye className="bg-inherit" />
                                )}
                            </div>
                        </div>

                        <div
                            className={`w-full h-[16px] flex items-center ${
                                incorrectCredentials ? "justify-between" : "justify-end"
                            }`}
                        >
                            {incorrectCredentials && (
                                <span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
                                    Incorrect Credentials
                                </span>
                            )}

                            <Link
                                to={"/forgot-password"}
                                className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-slategray underline"
                            >
                                Forgot password?
                            </Link>
                            {/* forgot-password link */}
                        </div>
                    </div>
                </form>

                <div className="h-[40px] max-w-[454px] w-full mt-[39px]">
                    <PrimaryButton>Login</PrimaryButton> {/* Use the PrimaryButton component */}
                </div>

                <div className="w-full h-[25.47px] flex justify-center mt-[25px] items-center">
                    <GoogleOauthButton /> {/* Use the GoogleOauthButton component */}
                </div>

                <div className="h-[25.47px] w-full flex justify-center mt-[46.26px]">
                    <span className="h-[17px] font-montserrat text-[14px] font-[400] leading-[10.07px] text-center">
                        Need a workspace?
                        <Link to={"/create-workspace"} className="underline text-primary">
                            Create a workspace
                        </Link>
                        {/* create-workspace link */}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default Login;
