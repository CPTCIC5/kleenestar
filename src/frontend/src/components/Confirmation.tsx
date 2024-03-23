import { FunctionComponent, useMemo, type CSSProperties } from "react";

export type ConfirmationType = {
  lastName?: string;
  lastNamePlaceholder?: string;

  /** Style props */
  propMinWidth?: CSSProperties["minWidth"];
  propWidth?: CSSProperties["width"];
};

const Confirmation: FunctionComponent<ConfirmationType> = ({
  lastName,
  lastNamePlaceholder,
  propMinWidth,
  propWidth,
}) => {
  const lastNameStyle: CSSProperties = useMemo(() => {
    return {
      minWidth: propMinWidth,
    };
  }, [propMinWidth]);

  const lastName1Style: CSSProperties = useMemo(() => {
    return {
      width: propWidth,
    };
  }, [propWidth]);

  return (
    <div className="self-stretch flex flex-col items-start justify-start py-0 pr-px pl-0 gap-[10.900000000000093px] text-left text-sm text-darkslateblue-100 font-montserrat">
      <div
        className="relative font-medium inline-block min-w-[79.7px] shrink-0 [debug_commit:f6aba90] z-[1]"
        style={lastNameStyle}
      >
        {lastName}
      </div>
      <div className="self-stretch flex flex-row items-start justify-start pt-[14.099999999999907px] px-[19.400000000000546px] pb-[14.600000000000136px] relative shrink-0 [debug_commit:f6aba90]">
        <input
          className="w-[84px] [border:none] [outline:none] font-montserrat text-mini bg-[transparent] h-[19.1px] relative text-darkslateblue-200 text-left inline-block p-0 z-[2]"
          placeholder={lastNamePlaceholder}
          type="text"
          style={lastName1Style}
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
  );
};

export default Confirmation;
