import { Eye, EyeOff } from "lucide-react";
import { FunctionComponent, useState } from "react";
import PrimaryInputBox from "../components/PrimaryInputBox";
import PrimaryButton from "../components/PrimaryButton";

const PasswordRecovery: FunctionComponent = () => {
    const [passwordShow1, setPasswordShow1] = useState<boolean>(false);
    const [passwordShow2, setPasswordShow2] = useState<boolean>(false);
    const [password, setPassword] = useState<string>("");
    const [confirmPassword, setConfirmPassword] = useState<string>("");
    const [passwordUnmatch, setPasswordUnmatch] = useState<boolean>(false);

    const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(event.target.value);
        if (event.target.value !== confirmPassword) {
            setPasswordUnmatch(true);
        } else {
            setPasswordUnmatch(false);
        }
    };

    const handleConfirmPasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setConfirmPassword(event.target.value);
        if (event.target.value !== password) {
            setPasswordUnmatch(true);
        } else {
            setPasswordUnmatch(false);
        }
    };

    const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log(password, confirmPassword);
        {
            /* add axios post request here */
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
            <div className="max-w-[722px] max-h-[552.63px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative bg-white ">
                <div className="max-width flex items-center justify-center box-border max-w-full">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
                            Password
                        </span>
                        <span className="max-w-[454px] w-full self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300">
                            Reset your password by creating a new one.
                        </span>
                    </div>
                </div>

                <form
                    method="post"
                    onSubmit={handleFormSubmit}
                    className={`max-w-[454px] w-full max-h-[434px] mt-[39px] flex flex-col items-center gap-[16px]`}
                >
                    <div className="w-full h-[72.33px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            New Password*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <PrimaryInputBox
                                type={passwordShow1 ? "text" : "password"}
                                placeholder="Password"
                                name="password"
                                onChange={handlePasswordChange}
                                className="focus:outline-primary-100 focus:outline"
                                value={password}
                                required
                            />
                            {/*PrimaryInputBox component for password*/}
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
                            passwordUnmatch ? "h-[99.66px]" : "h-[73.66px]"
                        } gap-[10px] flex flex-col justify-between`}
                    >
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Confirm Password*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <PrimaryInputBox
                                type={passwordShow2 ? "text" : "password"}
                                placeholder="Confirm Password"
                                name="confirm_password"
                                onChange={handleConfirmPasswordChange}
                                className="focus:outline-primary-100 focus:outline"
                                value={confirmPassword}
                                required
                            />
                            {/*PrimaryInputBox component for password*/}
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

                        {passwordUnmatch && (
                            <div className="w-full h-[16pxpx] flex items-center justify-start">
                                <span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
                                    {passwordUnmatch ? "Password doesn't match" : ""}
                                </span>
                            </div>
                        )}
                    </div>

                    <div className="h-[40px] max-w-[454px] w-full mt-[23px]">
                        <PrimaryButton disabled={passwordUnmatch || !password || !confirmPassword}>
                            Save password
                        </PrimaryButton>
                        {/* Use the PrimaryButton component */}
                    </div>
                </form>
            </div>
        </div>
    );
};

export default PasswordRecovery;
