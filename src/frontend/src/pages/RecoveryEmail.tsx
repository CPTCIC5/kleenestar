import { FunctionComponent, useState } from "react";
import PrimaryInputBox from "../components/PrimaryInputBox";
import { PencilLine } from "lucide-react";
import PrimaryButton from "../components/PrimaryButton";

const RecoveryEmail: FunctionComponent = () => {
    const [email, setEmail] = useState<string>("");
    const [unauthorisedEmail, setUnauthorisedEmail] = useState<boolean>(true);

    const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(event.target.value);
        const email = event.target.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            setUnauthorisedEmail(true);
        } else {
            setUnauthorisedEmail(false);
        }
    };

    const handleFormSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log(email);
        {
            /* add axios post request here */
        }
    };

    const handleSendCode = () => {
        {
            /* add send code request here */
        }
    };

    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4">
            <div className="max-w-[722px] max-h-[531.66px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative ">
                <div className="max-width flex items-center justify-center box-border max-w-full text-11xl font-syne">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[14px] max-w-full">
                        <span className=" m-0 text-inherit font-bold font-inherit inline-block z-[1]">
                            Recovery Email
                        </span>
                        <div className="max-w-[454px] self-stretch text-base text-center font-montserrat z-[1] flex flex-col item-center">
                            <span>
                                Send a password recovery email to your registered email address. 💁
                            </span>
                        </div>
                    </div>
                </div>

                <form
                    method="post"
                    onSubmit={handleFormSubmit}
                    className={`max-w-[454px] w-full max-h-[434px] mt-[39px] flex flex-col items-center gap-[16px]`}
                >
                    <div
                        className={`w-full  ${
                            unauthorisedEmail ? "h-[99.66px]" : "h-[73.66px]"
                        } gap-[10px] flex flex-col justify-between`}
                    >
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Email*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <PrimaryInputBox
                                type="email"
                                name="email"
                                placeholder="@work-email.com"
                                onChange={handleEmailChange}
                                className="focus:outline-primary-100 focus:outline"
                                value={email}
                                required
                            />
                            <div className="absolute bg-background text-primary flex items-center right-4">
                                <PencilLine className="bg-inherit" />
                            </div>
                        </div>

                        {unauthorisedEmail && (
                            <div className="w-full h-[16px] flex items-center justify-start">
                                <span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
                                    Email not recognized
                                </span>
                            </div>
                        )}
                    </div>
                    <div className="h-[40px] max-w-[454px] w-full mt-[23px]">
                        <PrimaryButton disabled={unauthorisedEmail || !email}>
                            Send email
                        </PrimaryButton>
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
