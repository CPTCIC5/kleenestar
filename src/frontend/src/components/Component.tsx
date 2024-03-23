import { FunctionComponent } from "react";

const Component: FunctionComponent = () => {
  return (
    <div className="self-stretch flex flex-row items-start justify-start gap-[11px] max-w-full z-[1] text-left text-sm text-darkslateblue-100 font-montserrat">
      <img
        className="h-[19px] w-[19px] relative min-h-[19px]"
        loading="lazy"
        alt=""
        src="/group-555.svg"
      />
      <div className="flex flex-col items-start justify-start pt-px px-0 pb-0">
        <div className="relative">
          Send me emails with tips, news, and offers.
        </div>
      </div>
    </div>
  );
};

export default Component;
