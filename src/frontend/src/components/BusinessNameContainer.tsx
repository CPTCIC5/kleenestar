import { FunctionComponent } from "react";
import "../global.css";
import {
  Select,
  InputLabel,
  MenuItem,
  FormHelperText,
  FormControl,
  InputAdornment,
} from "@mui/material";
import RoundArrowRightSvgrepoCom from "./RoundArrowRightSvgrepoCom";

const BusinessNameContainer: FunctionComponent = () => {
  
  return (
    <>
    <div className="flex-1 flex items-start justify-start pt-[21px] px-[25px] pb-[121px] box-border relative  min-w-[469px] max-w-full text-left text-sm text-darkslateblue-100 font-montserrat pl[400px">
     
      
      <div className="flex flex-1 items-center justify-center pt-[21px] px-[25px] pb-[121px] box-border relative min-w-[469px] max-w-full text-center text-sm text-darkslateblue-100 font-montserrat">
      <RoundArrowRightSvgrepoCom/>
        <div className="w-[454px] flex flex-col items-start justify-start gap-[39.666666666666664px] max-w-full mq450:gap-[20px_39.7px]">
          <div className="self-stretch flex flex-row items-start justify-start py-0 pr-2.5 pl-[9px] box-border max-w-full text-11xl font-syne">
            <div className="flex-1 flex flex-col items-start justify-start gap-[19px] max-w-full">
              <div className="self-stretch flex flex-row items-start justify-center py-0 px-5">
                <h1 className="m-0 relative text-inherit font-bold font-inherit z-[1] mq750:text-5xl mq450:text-lg">
                  Workspace
                </h1>
              </div>
              <div className="self-stretch flex flex-col items-end justify-start gap-[5px] text-center text-base font-montserrat">
                <div className="self-stretch relative z-[1]">{`The more Kleenestar knows the better it performs and `}</div>
                <div className="self-stretch flex flex-row items-start justify-center py-0 pr-5 pl-[29px]">
                  <div className="w-[218px] relative inline-block z-[1]">
                    help your business grow. 🤑
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="self-stretch flex flex-col items-start justify-start gap-[16.049999999999727px] z-[1]">
            <div className="self-stretch flex flex-col items-start justify-start gap-[10.300000000000182px]">
              <div className="relative font-medium inline-block min-w-[114px] shrink-0 [debug_commit:f6aba90]">
                Business name*
              </div>
              <div className="self-stretch flex flex-row items-start justify-start pt-[13.199999999999818px] px-[18.199999999999815px] pb-[13.800000000000182px] relative shrink-0 [debug_commit:f6aba90] text-mini text-darkslateblue-200">
                <div className="relative inline-block min-w-[115px] z-[1] ">
                  <input
                    type="text"
                    placeholder="Business name"
                    className="border border-gray-300 outline-none px-2 py-1"
                    style={{
                      width: "454px",
                      height: "45px",
                      flexShrink: 0,
                      fill: "#F8F9F7",
                      borderRadius: "4px",
                      border: "none",
                    }}
                  />
                  <img
                    className="absolute top-[50%] transform -translate-y-1/2 right-2 w-4 h-auto z-[2]"
                    alt=""
                    src="/pen2svgrepocom1.svg"
                  />
                </div>

                {/* <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">

                  <img
                    className="absolute top-[13px] left-[420.8px] w-[16.1px] h-[20.1px] z-[1]"
                    alt=""
                    src="/pen2svgrepocom1.svg"
                  />
                </div> */}
              </div>
            </div>
            <div className="self-stretch h-[72.3px] flex flex-col items-start justify-start pt-0 px-0 pb-[55.30000000000018px] box-border gap-[10.399999999999636px]">
              <div className="relative font-medium inline-block min-w-[64px] shrink-0 [debug_commit:f6aba90]">
                Website*
              </div>
              <div className="self-stretch flex flex-row items-start justify-start pt-[13.200000000000273px] px-[18.199999999999815px] pb-[13.799999999999727px] relative shrink-0 [debug_commit:f6aba90] text-mini text-darkslateblue-200">
                {/* <div className="relative inline-block min-w-[53px] z-[1]">
                  https://
                </div> */}
                <div className="relative inline-block min-w-[115px] z-[1] ">
                  <input
                    type="text"
                    placeholder="https://"
                    className="border border-gray-300 outline-none px-2 py-1"
                    style={{
                      width: "454px",
                      height: "45px",
                      flexShrink: 0,
                      fill: "#F8F9F7",
                      borderRadius: "4px",
                      border: "none",
                    }}
                  />
                  <img
                    className="absolute top-[50%] transform -translate-y-1/2 right-2 w-4 h-auto z-[2]"
                    alt=""
                    src="/pen2svgrepocom1.svg"
                  />
                </div>
                {/* <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
                  <img
                    className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
                    alt=""
                    src="/rectangle-522.svg"
                  />
                  <img
                    className="absolute top-[12.9px] left-[420.8px] w-[16.1px] h-[20.1px] z-[1]"
                    alt=""
                    src="/pen2svgrepocom1.svg"
                  />
                </div> */}
              </div>
            </div>
            <br />
            <div className="self-stretch flex flex-col items-start justify-start gap-[10.300000000000182px]">
              <div className="relative font-medium inline-block min-w-[60px] shrink-0 [debug_commit:f6aba90]">
                Industry
              </div>
              <FormControl
                className="self-stretch h-[45px] font-montserrat text-mini text-darkslateblue-200 shrink-0 [debug_commit:f6aba90]"
                variant="standard"
                sx={{
                  borderTopWidth: "0px",
                  borderRightWidth: "0px",
                  borderBottomWidth: "0px",
                  borderLeftWidth: "0px",
                  backgroundColor: "#f8f9f7",
                  borderRadius: "0px 0px 0px 0px",
                  width: "100%",
                  height: "45px",
                  m: 0,
                  p: 0,
                  "& .MuiInputBase-root": {
                    m: 0,
                    p: 0,
                    minHeight: "45px",
                    justifyContent: "center",
                    display: "inline-flex",
                  },
                  "& .MuiInputLabel-root": {
                    m: 0,
                    p: 0,
                    minHeight: "45px",
                    display: "inline-flex",
                  },
                  "& .MuiMenuItem-root": {
                    m: 0,
                    p: 0,
                    height: "45px",
                    display: "inline-flex",
                  },
                  "& .MuiSelect-select": {
                    m: 0,
                    p: 0,
                    height: "45px",
                    alignItems: "center",
                    display: "inline-flex",
                  },
                  "& .MuiInput-input": { m: 0, p: 0 },
                  "& .MuiInputBase-input": {
                    color: "rgba(28, 39, 76, 0.5)",
                    fontSize: 15,
                    fontWeight: "Regular",
                    fontFamily: "Montserrat",
                    textAlign: "left",
                    p: "0 !important",
                    marginLeft: "18.199999999999815px",
                  },
                }}
              >
                <InputLabel color="primary" />
                <Select
                  color="primary"
                  disableUnderline
                  displayEmpty
                  IconComponent={() => (
                    <img
                      width="11.5px"
                      height="5px"
                      src="/altarrowdownsvgrepocom.svg"
                      style={{ marginRight: "19.40000000000009px" }}
                    />
                  )}
                >
                  <MenuItem>What’s your industry?</MenuItem>
                </Select>
                <FormHelperText />
              </FormControl>
            </div>
          </div>
          <button
            className="cursor-pointer"
            style={{
              backgroundColor: "#1C274C",
              color: "white",
              borderRadius: "10px",
              width: "100%", // Set width to 100% for responsiveness
              height: "40px",
              flexShrink: 0,
              border: "none", // If you want to remove the border
              padding: 0, // If you want to remove padding
              alignSelf: "stretch", // If you want the button to stretch vertically
              position: "relative", // If you want to position child elements absolutely
              maxWidth: "454px", // Set maximum width for larger screens
              margin: "0 auto", // Center the button horizontally
            }}
          >
            Create
          </button>

          <div className="self-stretch flex flex-row items-start justify-start py-0 pr-[9px] pl-2.5 box-border max-w-full text-center">
            <div className="flex-1 flex flex-col items-end justify-start gap-[3px] max-w-full">
              <div className="self-stretch relative z-[1]">
                {`By continuing, you’re agreeing to our `}
                <span className="[text-decoration:underline]">
                  Terms of Service
                </span>
                {`, `}
                <span className="[text-decoration:underline]">{`Privacy `}</span>
              </div>
              <div className="w-[420.4px] flex flex-row items-start justify-center py-0 px-5 box-border max-w-full">
                <div className="w-[175px] relative [text-decoration:underline] inline-block z-[1]">
                  Policy, and Cookie Policy.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </>
  );
};

export default BusinessNameContainer;
