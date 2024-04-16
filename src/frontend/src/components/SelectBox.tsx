import React from "react";
import CustomSelect from "./CustomSelect";
import { FieldValues, SubmitHandler, useForm } from "react-hook-form";

const SelectBox: React.FunctionComponent = () => {
    const { control, handleSubmit } = useForm({
        mode: "onChange", // This will validate the form on each input's change
    });

    const options = [
        { value: "apple", label: "Apple" },
        { value: "banana", label: "Banana" },
        { value: "orange", label: "Orange" },
    ];

    const onSubmit: SubmitHandler<FieldValues> = (data) => {
        console.log(data);
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <div className="mb-10 w-full  flex justify-center items-center">
                <div className="max-w-[400px] w-full h-[40px]">
                    <CustomSelect name="mySelect" control={control} options={options} />
                </div>
            </div>
            <button type="submit">Submit</button>
        </form>
    );
};

export default SelectBox;
