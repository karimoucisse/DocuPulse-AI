import { useState } from "react";
import LeftSidebar from "../components/sidebar/LeftSidebar"
import RightSidebar from "../components/sidebar/RightSidebar"
import { IoSendSharp } from "react-icons/io5";
import axios from "axios";
const Prompt = () => {
	const [message, setMessage] = useState("");
	const [response, setResponse] = useState("");

	const handleSendMessage = async (message) => {
		try {
			setMessage("");
			const res = await axios.post("http://localhost:8000/question", {question: message}, {
				headers: {
					"Content-Type": "application/json",
				},
			})
			const _response = res.data;
			setResponse(_response);
		} catch (error) {
			console.error("Error sending message:", error);
		}
	}
  return (
	<div className="flex">
		{/* <Header/> */}
		<LeftSidebar/>
		<div className="flex flex-col flex-2 justify-between p-6">
			<div className="flex-1 overflow-y-auto py-6">
				<p>{response?.answer}</p>
			</div>
			<div className="flex items-center w-full relative border rounded-xl h-15">
				<textarea
					onChange={(e) => setMessage(e.target.value)}
					value={message}
					maxLength="2000"
					placeholder="Posez une question ..."
					id="message-input"
					name="message"
					autoComplete="off"
					rows="1"
					className="flex-1  h-full resize-none outline-none text-sm placeholder-gray-500 py-2 px-5"
				>
				</textarea>
				<button onClick={() => handleSendMessage(message)} className="btn bg-primary btn-sm ml-2 absolute right-5 text-lg"><IoSendSharp /></button>
			</div>
		</div>
		{response && <RightSidebar sources = {response?.sources}/>}
		{/* <RightSidebar sources = {response?.sources}/> */}
	</div>
  )
}

export default Prompt
