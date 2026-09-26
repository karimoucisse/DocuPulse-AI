import Header from "../components/Header"
import Sidebar from "../components/Sidebar"

const Prompt = () => {
  return (
	<div>
		<Header/>
		<div className="flex p-4">
			<Sidebar/>
			<div className="flex flex-2 items-end h-full p-4">
				<textarea
					maxLength="2000"
					placeholder="Posez une question ..."
					id="message-input"
					name="message"
					autoComplete="off"
					rows="1"
					className="flex-1 border h-15 rounded-2xl bg-transparent resize-none outline-none text-sm placeholder-gray-500 py-2 px-5"
				></textarea>
			</div>
			<Sidebar/>
		</div>
	</div>
  )
}

export default Prompt
