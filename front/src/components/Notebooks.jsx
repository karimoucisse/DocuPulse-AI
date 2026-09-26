import { Notebook } from "./Notebook"

const Notebooks = () => {
  return (
    <div className="w-full mt-10">
      <div className="flex justify-between mb-6">
        <p>NoteBooks</p>
        <button className="btn btn-primary btn-sm">Nouveau notebook</button>
      </div>
      <div className="flex justify-between flex-wrap gap-6">
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
        <Notebook name="Python" creation_date="20 sept. 2026" number_source={14}/>
      </div>
    </div>
  )
}

export default Notebooks
