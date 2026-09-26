import { FaBookOpen } from "react-icons/fa";
import { IoMdMore } from "react-icons/io";

export const Notebook = ({name, creation_date, number_source}) => {
  return (
	  <div className="flex flex-col justify-between h-40 w-50 rounded-xl p-4 bg-primary
      shadow-xl">
      <div className="flex justify-between items-start mb-4">
        <FaBookOpen className="text-5xl"/>
        <IoMdMore className="text-xl cursor-pointer"/>
      </div>
      <div className="text-sm">
        <p className="text-lg">{name}</p>
        <div className="text-xs flex">
          <p>{creation_date} - </p>
          <p>{number_source} sources</p>
        </div>
      </div>
    </div>
  )
}

