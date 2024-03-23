import { FunctionComponent } from "react";
import Confirmation from "./Confirmation";

const PasswordUpdate: FunctionComponent = () => {
  return (
    <div className="flex-[0.9123] flex flex-col items-start justify-start pt-[26.600000000000136px] px-[27.600000000000364px] pb-[29.79999999999984px] box-border relative gap-[180.4000000000001px] min-w-[409px] max-w-full text-left text-lg text-darkslateblue-100 font-montserrat lg:flex-1 mq750:gap-[90px_180.4px] mq750:pt-5 mq750:pb-5 mq750:box-border mq750:min-w-full mq450:gap-[45px_180.4px]">
      <div className="w-[208.1px] flex flex-col items-start justify-start gap-[11.599999999999907px]">
        <div className="relative font-semibold inline-block min-w-[64.8px] z-[1]">
          Profile
        </div>
        <div className="self-stretch flex flex-row items-start justify-start py-0 pr-0 pl-[1.899999999999636px] text-sm">
          <div className="flex-1 relative z-[1]">
            Manage your profile details.
          </div>
        </div>
      </div>
      <div className="self-stretch flex flex-col items-end justify-start gap-[29.40000000000009px] text-sm">
        <div className="self-stretch flex flex-row items-start justify-start gap-[17.100000000000364px] mq750:flex-wrap">
          <div className="flex-1 flex flex-col items-start justify-start gap-[17.600000000000023px] min-w-[181px]">
            <div className="self-stretch flex flex-col items-start justify-start py-0 pr-px pl-0 gap-[10.900000000000093px]">
              <div className="relative font-medium inline-block min-w-[81.8px] shrink-0 [debug_commit:f6aba90] z-[1]">
                First name
              </div>
              <div className="self-stretch flex flex-row items-start justify-start pt-[14.099999999999907px] px-[19.300000000000185px] pb-[14.600000000000136px] relative shrink-0 [debug_commit:f6aba90]">
                <input
                  className="w-[86.1px] [border:none] [outline:none] font-montserrat text-mini bg-[transparent] h-[19.1px] relative text-darkslateblue-200 text-left inline-block p-0 z-[2]"
                  placeholder="First name"
                  type="text"
                />
                <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
                  <img
                    className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
                    alt=""
                    src="/rectangle-522.svg"
                  />
                  <img
                    className="absolute top-[13.8px] left-[242.7px] w-[17.1px] h-[21.3px] z-[2]"
                    alt=""
                    src="/pen2svgrepocom.svg"
                  />
                </div>
              </div>
            </div>
            <div className="self-stretch flex flex-col items-start justify-start py-0 pr-px pl-0 gap-[10.900000000000093px]">
              <div className="relative font-medium inline-block min-w-[106.3px] shrink-0 [debug_commit:f6aba90] z-[1]">
                Email address
              </div>
              <div className="self-stretch h-[47.8px] relative shrink-0 [debug_commit:f6aba90]">
                <img
                  className="absolute top-[0px] left-[0px] w-[278px] h-[47.8px] z-[1]"
                  alt=""
                  src="/rectangle-522-1.svg"
                />
                <input
                  className="w-full [border:none] [outline:none] font-montserrat text-mini bg-[transparent] absolute top-[14.1px] left-[19.3px] text-darkslateblue-100 text-left inline-block h-[19.1px] whitespace-nowrap p-0 z-[2]"
                  placeholder="craig.c@kleenestar.io"
                  type="text"
                />
              </div>
            </div>
            <div className="self-stretch flex flex-col items-start justify-start gap-[10.899999999999975px]">
              <div className="relative font-medium inline-block min-w-[61.6px] z-[1]">
                Country
              </div>
              <div className="self-stretch flex flex-row items-start justify-start pt-[14.100000000000025px] px-[19.399999999999636px] pb-[14.599999999999907px] relative text-mini text-darkslateblue-200">
                <div className="relative inline-block min-w-[64.8px] z-[2]">
                  Country
                </div>
                <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
                  <img
                    className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
                    alt=""
                    src="/rectangle-522.svg"
                  />
                  <img
                    className="absolute top-[21.8px] left-[245.1px] w-[12.3px] h-[5.3px] z-[2]"
                    loading="lazy"
                    alt=""
                    src="/altarrowdownsvgrepocom.svg"
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="flex-1 flex flex-col items-end justify-start gap-[17.600000000000023px] min-w-[181px]">
            <Confirmation
              lastName="Last name"
              lastNamePlaceholder="Last name"
            />
            <Confirmation
              lastName="Workspace name"
              lastNamePlaceholder="Workspace name"
              propMinWidth="unset"
              propWidth="140.3px"
            />
            <div className="self-stretch flex flex-col items-start justify-start gap-[10.899999999999975px]">
              <div className="relative font-medium inline-block min-w-[115.9px] z-[1]">
                Phone number
              </div>
              <div className="self-stretch flex flex-row items-start justify-start pt-[14.100000000000025px] px-[19.400000000000546px] pb-[14.599999999999907px] relative">
                <input
                  className="w-[110.5px] [border:none] [outline:none] font-inter text-mini bg-[transparent] h-[19.1px] relative text-darkslateblue-200 text-left inline-block p-0 z-[2]"
                  placeholder="Phone number"
                  type="text"
                />
                <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
                  <img
                    className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
                    alt=""
                    src="/rectangle-522.svg"
                  />
                  <img
                    className="absolute top-[13.8px] left-[242.7px] w-[17.1px] h-[21.3px] z-[2]"
                    alt=""
                    src="/pen2svgrepocom-1.svg"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <button className="cursor-pointer [border:none] p-0 bg-[transparent] self-stretch h-[42.5px] relative">
          <img
            className="absolute top-[0px] left-[0px] w-[573.6px] h-[42.5px] z-[1]"
            alt=""
            src="/rectangle-512.svg"
          />
          <div className="absolute top-[10.7px] left-[230.3px] text-mini font-medium font-montserrat text-whitesmoke text-left inline-block w-[111.6px] h-[19.1px] z-[2]">
            Save changes
          </div>
        </button>
      </div>
      <div className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
        <img
          className="absolute h-full w-[calc(100%_-_1px)] top-[0px] right-[0.5px] bottom-[0px] left-[0.5px] max-w-full overflow-hidden max-h-full"
          alt=""
          src="/rectangle-516.svg"
        />
        <img
          className="absolute top-[123.3px] left-[27.8px] w-[109.8px] h-[109.8px] z-[1]"
          loading="lazy"
          alt=""
          src="/group-2119.svg"
        />
        <img
          className="absolute top-[167.6px] left-[154.6px] w-[21.3px] h-[21.3px] z-[1]"
          loading="lazy"
          alt=""
          src="/gallerysendsvgrepocom.svg"
        />
        <img
          className="absolute top-[102px] left-[0px] w-[629.3px] h-px z-[1]"
          alt=""
          src="/line-107.svg"
        />
      </div>
    </div>
  );
};

export default PasswordUpdate;
